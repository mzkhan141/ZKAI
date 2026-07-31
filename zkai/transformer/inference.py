"""Inference Engine managing streaming, batching, and KV Cache generation loops."""

from typing import Callable, Generator, List, Optional
import torch
from zkai.neural.tensor import Tensor
from zkai.transformer.decoder import Decoder
from zkai.transformer.tokenizer import Tokenizer
from zkai.transformer.sampling import Sampler, TopPSampler, RepetitionPenalty
from zkai.transformer.kv_cache import KVCache
from zkai.core.logger import get_logger

logger = get_logger("transformer.inference")


class InferenceEngine:
    """Inference Engine for native ZKAI Foundation Models."""

    def __init__(self, model: Decoder, tokenizer: Optional[Tokenizer] = None):
        self.model = model
        self.tokenizer = tokenizer or Tokenizer()
        self.model.eval()

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 128,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repetition_penalty: float = 1.1,
        sampler: Optional[Sampler] = None,
    ) -> str:
        """Generates text completion for a given input prompt string."""
        prompt_ids = self.tokenizer.encode(prompt)
        generated = list(prompt_ids)

        active_sampler = sampler or TopPSampler(p=top_p, temperature=temperature)

        # Initialize KV Caches for layers
        kv_caches = [
            KVCache(
                max_batch_size=1,
                max_seq_len=len(prompt_ids) + max_new_tokens + 10,
                num_kv_heads=self.model.config.num_kv_heads or self.model.config.num_heads,
                head_dim=self.model.config.head_dim,
                device=self.model.norm.weight.device,
            )
            for _ in range(self.model.config.num_layers)
        ]

        curr_pos = 0
        input_ids = Tensor(torch.tensor([prompt_ids]))

        for _ in range(max_new_tokens):
            with torch.no_grad():
                logits = self.model(input_ids, start_pos=curr_pos, kv_caches=kv_caches)
                next_token_logits = logits.raw[:, -1, :]
                next_token_logits = RepetitionPenalty.apply(next_token_logits, generated, penalty=repetition_penalty)

                next_token = active_sampler.sample(Tensor(next_token_logits))
                generated.append(next_token)

                if next_token == self.tokenizer._hf_tokenizer.token_to_id("</s>"):
                    break

                curr_pos += input_ids.shape[1]
                input_ids = Tensor(torch.tensor([[next_token]]))

        return self.tokenizer.decode(generated[len(prompt_ids):])

    def generate_stream(
        self,
        prompt: str,
        max_new_tokens: int = 128,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """Yields token strings sequentially as they are decoded."""
        prompt_ids = self.tokenizer.encode(prompt)
        generated = list(prompt_ids)
        sampler = TopPSampler(temperature=temperature)

        input_ids = Tensor(torch.tensor([prompt_ids]))
        curr_pos = 0

        for _ in range(max_new_tokens):
            with torch.no_grad():
                logits = self.model(input_ids, start_pos=curr_pos)
                next_token_logits = logits.raw[:, -1, :]
                next_token = sampler.sample(Tensor(next_token_logits))
                generated.append(next_token)

                token_text = self.tokenizer.decode([next_token])
                yield token_text

                if next_token == self.tokenizer._hf_tokenizer.token_to_id("</s>"):
                    break

                curr_pos += input_ids.shape[1]
                input_ids = Tensor(torch.tensor([[next_token]]))


    def generate_continuous(self, prompts: List[str], max_new_tokens: int = 128) -> List[str]:
        """Generates text completions using continuous batching iteration engine."""
        from zkai.transformer.continuous_batcher import ContinuousBatcher
        batcher = ContinuousBatcher(max_batch_size=len(prompts))
        reqs = []
        for idx, prompt in enumerate(prompts):
            p_ids = self.tokenizer.encode(prompt)
            req = batcher.add_request(f"req_{idx}", p_ids, max_new_tokens=max_new_tokens)
            reqs.append(req)

        while any(not r.is_finished for r in reqs):
            batcher.step()

        results = []
        for req in reqs:
            decoded = self.tokenizer.decode(req.generated_tokens)
            results.append(decoded)
        return results


class BatchInference:
    """Batch inference processor for high-throughput batch generation."""

    def __init__(self, engine: InferenceEngine):
        self.engine = engine

    def process_batch(self, prompts: List[str]) -> List[str]:
        return [self.engine.generate(p) for p in prompts]

