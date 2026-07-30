"""GPUSynchronizer providing all-reduce and barrier primitives."""

import torch
import torch.distributed as dist


class GPUSynchronizer:
    """Multi-GPU communication primitives: all_reduce, broadcast, barrier."""

    @staticmethod
    def barrier() -> None:
        if dist.is_initialized():
            dist.barrier()

    @staticmethod
    def all_reduce(tensor: torch.Tensor, op=dist.ReduceOp.SUM) -> torch.Tensor:
        if dist.is_initialized():
            dist.all_reduce(tensor, op=op)
        return tensor

    @staticmethod
    def broadcast(tensor: torch.Tensor, src: int = 0) -> torch.Tensor:
        if dist.is_initialized():
            dist.broadcast(tensor, src=src)
        return tensor
