"""Weight packing utilities for sub-byte quantized weights."""

import torch


class WeightPacker:
    """Packs two 4-bit integer values into a single uint8 byte container."""

    @staticmethod
    def pack_int4_to_uint8(int4_tensor: torch.Tensor) -> torch.Tensor:
        flattened = int4_tensor.flatten()
        if flattened.numel() % 2 != 0:
            flattened = torch.cat([flattened, torch.zeros(1, dtype=flattened.dtype, device=flattened.device)])
        uint_tensor = (flattened + 8).to(torch.uint8)
        packed = (uint_tensor[0::2] << 4) | (uint_tensor[1::2] & 0x0F)
        return packed

    @staticmethod
    def unpack_uint8_to_int4(packed_tensor: torch.Tensor, original_shape: torch.Size) -> torch.Tensor:
        high = (packed_tensor >> 4).to(torch.int8) - 8
        low = (packed_tensor & 0x0F).to(torch.int8) - 8
        unpacked = torch.stack([high, low], dim=-1).flatten()
        return unpacked[: original_shape.numel()].reshape(original_shape)
