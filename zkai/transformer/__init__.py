"""Modern Transformer Architecture, Tokenization, and Inference Engine for ZKAI."""

from zkai.transformer.tokenizer import Tokenizer, Vocabulary, BytePairEncoding
from zkai.transformer.embeddings import TokenEmbedding, RotaryEmbedding, PositionalEncoding, ALiBi
from zkai.transformer.attention import MultiHeadAttention, SelfAttention, CrossAttention, FlashAttention
from zkai.transformer.feedforward import FeedForward, GatedFeedForward, MoEFeedForward
from zkai.transformer.block import TransformerBlock
from zkai.transformer.encoder import Encoder
from zkai.transformer.decoder import Decoder
from zkai.transformer.kv_cache import KVCache, PagedKVCache
from zkai.transformer.sampling import GreedySampler, TopKSampler, TopPSampler, TemperatureSampler, BeamSearch, RepetitionPenalty
from zkai.transformer.inference import InferenceEngine, BatchInference

from zkai.transformer.continuous_batcher import ContinuousBatcher, DynamicBatchScheduler, SequenceScheduler
from zkai.transformer.prefill_decode import PrefillEngine, DecodeEngine
from zkai.transformer.speculative import SpeculativeDecoding
from zkai.transformer.kv_memory import KVMemoryManager, PrefixCache
from zkai.transformer.token_streamer import TokenStreamer, StreamingGeneration

__all__ = [
    "Tokenizer",
    "Vocabulary",
    "BytePairEncoding",
    "TokenEmbedding",
    "RotaryEmbedding",
    "PositionalEncoding",
    "ALiBi",
    "MultiHeadAttention",
    "SelfAttention",
    "CrossAttention",
    "FlashAttention",
    "FeedForward",
    "GatedFeedForward",
    "MoEFeedForward",
    "TransformerBlock",
    "Encoder",
    "Decoder",
    "KVCache",
    "PagedKVCache",
    "GreedySampler",
    "TopKSampler",
    "TopPSampler",
    "TemperatureSampler",
    "BeamSearch",
    "RepetitionPenalty",
    "InferenceEngine",
    "BatchInference",
    "ContinuousBatcher",
    "DynamicBatchScheduler",
    "SequenceScheduler",
    "PrefillEngine",
    "DecodeEngine",
    "SpeculativeDecoding",
    "KVMemoryManager",
    "PrefixCache",
    "TokenStreamer",
    "StreamingGeneration",
]

