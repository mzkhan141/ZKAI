"""VisionEncoder (Vision Transformer / ViT patch embedding encoder)."""

import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.vision.image import Image


class VisionEncoder(Module):
    """Vision Transformer (ViT) patch encoder mapping images to token embeddings."""

    def __init__(self, image_size: int = 224, patch_size: int = 16, in_channels: int = 3, embed_dim: int = 768):
        super().__init__()
        self.image_size = image_size
        self.patch_size = patch_size
        self.num_patches = (image_size // patch_size) ** 2

        self.patch_embed = nn.Conv2d(
            in_channels, embed_dim, kernel_size=patch_size, stride=patch_size
        )
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, self.num_patches + 1, embed_dim))

    def forward(self, x: Tensor) -> Tensor:
        # x: (batch, 3, image_size, image_size)
        bsz = x.shape[0]
        patches = self.patch_embed(x.raw).flatten(2).transpose(1, 2)
        cls_tokens = self.cls_token.expand(bsz, -1, -1)
        tokens = torch.cat((cls_tokens, patches), dim=1)
        out = tokens + self.pos_embed
        return Tensor(out)
