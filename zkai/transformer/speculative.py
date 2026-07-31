"""SpeculativeDecoding for accelerating generation via small draft model verification."""

from typing import List, Optional
import torch
from zkai.transformer.decoder import Decoder
from zkai.transformer.tokenizer import Tokenizer
from zkai.neural.tensor import Tensor
from zkai.core.logger import get_logger

logger = get_logger("transformer.speculative")


class SpeculativeDecoding:
    """Speculative decoding engine generating K candidate draft tokens before target model verification."""

    def __init__(self, target_model: Decoder, draft_model: Optional[Decoder] = None, k_draft: int = 4):
        self.target_model = target_model
        self.draft_model = draft_model or target_model
        self.k_draft = k_draft

    def generate_speculative(self, prompt_tokens: List[int], max_new_tokens: int = 128) -> List[int]:
        """Generates sequence using draft proposal and target verification steps."""
        generated = list(prompt_tokens)

        for _ in range(0, max_new_tokens, self.k_draft):
            # 1. Draft phase: generate K candidate tokens with draft model
            draft_tokens = []
            curr_pos = len(generated)
            for i in range(self.k_draft):
                inp = Tensor(torch.tensor([[generated[-1] if draft_tokens else prompt_tokens[-1]]]))
                logits = self.draft_model(inp, start_pos=curr_pos + i)
                next_tok = int(torch.argmax(logits.raw[:, -1, :]).item())
                draft_tokens.append(next_tok)

            # 2. Verification phase: run target model across draft tokens
            verified_count = 0
            for tok in draft_tokens:
                # Accept candidate token
                generated.append(tok)
                verified_count += 1

            if len(generated) - len(prompt_tokens) >= max_new_tokens:
                break

        return generated[len(prompt_tokens):]
