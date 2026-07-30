"""Unit tests for zkai.transformer components."""

import pytest
import torch
from zkai.transformer.tokenizer import Tokenizer, Vocabulary
from zkai.transformer.embeddings import TokenEmbedding, RotaryEmbedding
from zkai.transformer.attention import MultiHeadAttention
from zkai.transformer.feedforward import FeedForward
from zkai.transformer.block import TransformerBlock
from zkai.transformer.decoder import Decoder
from zkai.neural.tensor import Tensor
from zkai.core.config import TransformerConfig


def test_vocabulary():
    vocab = Vocabulary()
    idx = vocab.add_token("hello")
    assert vocab.id_to_token[idx] == "hello"
    assert len(vocab) == 5  # 4 special + 1 custom


def test_rotary_embedding():
    rope = RotaryEmbedding(dim=64)
    q = torch.randn(1, 4, 10, 64)
    k = torch.randn(1, 4, 10, 64)
    q_rot, k_rot = rope(q, k, seq_len=10)
    assert q_rot.shape == (1, 4, 10, 64)


def test_multi_head_attention():
    mha = MultiHeadAttention(hidden_dim=128, num_heads=4)
    x = Tensor(torch.randn(2, 8, 128))
    out = mha(x)
    assert out.shape == (2, 8, 128)


def test_transformer_block():
    block = TransformerBlock(hidden_dim=64, num_heads=2)
    x = Tensor(torch.randn(1, 6, 64))
    out = block(x)
    assert out.shape == (1, 6, 64)


def test_decoder_model():
    cfg = TransformerConfig(vocab_size=1000, hidden_dim=64, num_layers=2, num_heads=2)
    decoder = Decoder(config=cfg)
    input_ids = Tensor(torch.randint(0, 1000, (1, 5)))
    logits = decoder(input_ids)
    assert logits.shape == (1, 5, 1000)
