"""TokenPacker for packing multiple short sequences into full max-length context blocks."""

from typing import Any, Dict, List, Tuple
import torch
from zkai.neural.tensor import Tensor


class TokenPacker:
    """Sequence packer concatenating token sequences into target context lengths."""

    def __init__(self, max_seq_len: int = 2048, pad_token_id: int = 0, eos_token_id: int = 2):
        self.max_seq_len = max_seq_len
        self.pad_token_id = pad_token_id
        self.eos_token_id = eos_token_id

    def pack_sequences(self, sequences: List[List[int]]) -> List[Dict[str, Tensor]]:
        """Packs variable length token sequences into fixed max_seq_len batches."""
        packed_batches: List[Dict[str, Tensor]] = []
        current_input_ids: List[int] = []
        current_labels: List[int] = []

        for seq in sequences:
            tokens = seq + [self.eos_token_id] if seq[-1] != self.eos_token_id else list(seq)

            while len(tokens) > 0:
                available_space = self.max_seq_len - len(current_input_ids)
                chunk = tokens[:available_space]
                tokens = tokens[available_space:]

                current_input_ids.extend(chunk)

                if len(current_input_ids) == self.max_seq_len:
                    input_t = torch.tensor(current_input_ids, dtype=torch.long)
                    target_t = torch.cat([input_t[1:], torch.tensor([self.eos_token_id], dtype=torch.long)])
                    packed_batches.append({
                        "input_ids": Tensor(input_t.unsqueeze(0)),
                        "labels": Tensor(target_t.unsqueeze(0)),
                    })
                    current_input_ids = []

        if current_input_ids:
            pad_len = self.max_seq_len - len(current_input_ids)
            input_ids = current_input_ids + [self.pad_token_id] * pad_len
            input_t = torch.tensor(input_ids, dtype=torch.long)
            target_t = torch.cat([input_t[1:], torch.tensor([self.pad_token_id], dtype=torch.long)])
            packed_batches.append({
                "input_ids": Tensor(input_t.unsqueeze(0)),
                "labels": Tensor(target_t.unsqueeze(0)),
            })

        return packed_batches
