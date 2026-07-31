"""PrefillEngine and DecodeEngine separating prompt prefill phase from token decode phase."""

from typing import List, Optional, Tuple
import torch
from zkai.neural.tensor import Tensor
from zkai.transformer.decoder import Decoder
from zkai.transformer.kv_cache import KVCache
from zkai.core.logger import get_logger

logger = get_logger("transformer.prefill_decode")


class PrefillEngine:
    """Prefill engine processing prompt tokens in parallel to populate KV cache."""

    def __init__(self, model: Decoder):
        self.model = model

    def prefill(self, prompt_tokens: List[int], kv_caches: List[KVCache]) -> Tensor:
        """Processes full prompt sequence in parallel, initializing KV cache buffers."""
        input_tensor = Tensor(torch.tensor([prompt_tokens]))
        with torch.no_grad():
            logits = self.model(input_tensor, start_pos=0, kv_caches=kv_caches)
        return logits


class DecodeEngine:
    """Decode engine executing single autoregressive token generation steps."""

    def __init__(self, model: Decoder):
        self.model = model

    def decode_step(self, next_token: int, start_pos: int, kv_caches: List[KVCache]) -> Tensor:
        """Executes single token forward step utilizing cached KV keys/values."""
        input_tensor = Tensor(torch.tensor([[next_token]]))
        with torch.no_grad():
            logits = self.model(input_tensor, start_pos=start_pos, kv_caches=kv_caches)
        return logits
