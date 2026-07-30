"""Model Metadata and Model Card declarations."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class ModelMetadata:
    """Structure holding model attributes, configuration, and capabilities."""
    name: str = "zkai_model"
    architecture: str = "DecoderTransformer"
    num_parameters: int = 0
    vocab_size: int = 32000
    hidden_dim: int = 4096
    num_layers: int = 32
    num_heads: int = 32
    format: str = "zk"
    version: str = "1.0.0"
    created_at: str = ""
    author: str = "ZKAI"
    license: str = "MIT"
    tags: List[str] = field(default_factory=list)
    custom_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelCard:
    """Documentation card for model artifacts."""
    metadata: ModelMetadata
    description: str = ""
    usage_example: str = ""
    limitations: str = ""
