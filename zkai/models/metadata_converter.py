"""MetadataConverter converting model metadata between container format standards."""

from typing import Any, Dict
from zkai.models.metadata import ModelMetadata


class MetadataConverter:
    """Metadata converter standardizing headers across GGUF, HuggingFace config.json, and .zk metadata."""

    @staticmethod
    def from_hf_config(config_dict: Dict[str, Any], model_name: str = "hf_model") -> ModelMetadata:
        """Converts HuggingFace config.json dict into ModelMetadata."""
        return ModelMetadata(
            name=model_name,
            architecture=config_dict.get("architectures", ["DecoderTransformer"])[0] if isinstance(config_dict.get("architectures"), list) else "DecoderTransformer",
            num_parameters=config_dict.get("num_parameters", 0),
            vocab_size=config_dict.get("vocab_size", 32000),
            hidden_dim=config_dict.get("hidden_size") or config_dict.get("d_model", 4096),
            num_layers=config_dict.get("num_hidden_layers") or config_dict.get("n_layer", 32),
            num_heads=config_dict.get("num_attention_heads") or config_dict.get("n_head", 32),
            custom_config=config_dict,
        )

    @staticmethod
    def to_gguf_metadata(meta: ModelMetadata) -> Dict[str, Any]:
        """Converts ModelMetadata into GGUF header dictionary format."""
        return {
            "general.name": meta.name,
            "general.architecture": meta.architecture,
            "llama.block_count": meta.num_layers,
            "llama.embedding_length": meta.hidden_dim,
            "llama.attention.head_count": meta.num_heads,
            "llama.vocab_size": meta.vocab_size,
        }
