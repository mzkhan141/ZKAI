"""ZKModelFormat providing native .zk file creation, parsing, and validation."""

from pathlib import Path
from typing import Any, Dict, Tuple
from zkai.core.serialization import ZKSerializer, ZKHeader
from zkai.models.metadata import ModelMetadata
from zkai.core.exceptions import ModelError
from zkai.core.logger import get_logger

logger = get_logger("models.format_zk")


class ZKModelFormat:
    """Formatter and loader for native ZKAI .zk binary model containers."""

    @staticmethod
    def save_model(file_path: str, model_state_dict: Dict[str, Any], metadata: ModelMetadata) -> str:
        """Saves a model state dictionary and metadata into a .zk file."""
        header = ZKHeader(
            model_name=metadata.name,
            architecture=metadata.architecture,
            parameter_count=metadata.num_parameters,
            format_version=1,
            metadata={
                "vocab_size": metadata.vocab_size,
                "hidden_dim": metadata.hidden_dim,
                "num_layers": metadata.num_layers,
                "num_heads": metadata.num_heads,
                "version": metadata.version,
                "author": metadata.author,
                "tags": metadata.tags,
            },
        )
        # Convert state_dict values to raw binary buffer
        tensor_bytes = bytearray()
        for key, value in model_state_dict.items():
            if hasattr(value, "numpy"):
                tensor_bytes.extend(value.numpy().tobytes())

        ZKSerializer.write_zk_file(file_path, header, bytes(tensor_bytes))
        logger.info(f"Saved .zk model to {file_path}")
        return file_path

    @staticmethod
    def load_model(file_path: str) -> Tuple[ModelMetadata, bytes]:
        """Loads and verifies a .zk model artifact."""
        header, tensor_payload, _ = ZKSerializer.read_zk_file(file_path)
        meta = ModelMetadata(
            name=header.model_name,
            architecture=header.architecture,
            num_parameters=header.parameter_count,
            vocab_size=header.metadata.get("vocab_size", 32000),
            hidden_dim=header.metadata.get("hidden_dim", 4096),
            num_layers=header.metadata.get("num_layers", 32),
            num_heads=header.metadata.get("num_heads", 32),
            version=header.metadata.get("version", "1.0.0"),
            tags=header.metadata.get("tags", []),
        )
        return meta, tensor_payload
