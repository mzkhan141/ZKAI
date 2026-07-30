"""Prompt Tuning soft prompt embedding vectors."""

import torch
import torch.nn as nn


class PromptTuning(nn.Module):
    """Learns virtual prompt token embeddings prepended to input sequences."""

    def __init__(self, prompt_tokens: int = 8, embed_dim: int = 768):
        super().__init__()
        self.prompt_tokens = prompt_tokens
        self.soft_prompts = nn.Parameter(torch.randn(prompt_tokens, embed_dim))

    def forward(self, input_embeds: torch.Tensor) -> torch.Tensor:
        batch_size = input_embeds.shape[0]
        prompts = self.soft_prompts.unsqueeze(0).expand(batch_size, -1, -1)
        return torch.cat([prompts, input_embeds], dim=1)
