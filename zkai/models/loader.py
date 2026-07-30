"""ModelLoader supporting PyTorch, Safetensors, GGUF, ONNX, HF, and native .zk format."""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import torch
from zkai.transformer.decoder import Decoder
from zkai.models.format_zk import ZKModelFormat
from zkai.core.types import ModelFormat
from zkai.core.exceptions import ModelError
from zkai.core.logger import get_logger

logger = get_logger("models.loader")


class ModelLoader:
    """Loader loading model weights across multiple binary container formats."""

    @staticmethod
    def detect_format(file_path: str) -> ModelFormat:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == ".zk":
            return ModelFormat.ZK
        elif suffix == ".safetensors":
            return ModelFormat.SAFETENSORS
        elif suffix in [".pt", ".pth", ".bin"]:
            return ModelFormat.PYTORCH
        elif suffix == ".gguf":
            return ModelFormat.GGUF
        elif suffix == ".onnx":
            return ModelFormat.ONNX
        return ModelFormat.ZK

    def load(self, file_path: str, device: str = "cpu") -> Tuple[Any, Dict[str, Any]]:
        """Loads model state dictionary and metadata from any supported format."""
        fmt = self.detect_format(file_path)
        logger.info(f"Loading model '{file_path}' using format detector: {fmt.value}")

        if fmt == ModelFormat.ZK:
            metadata, payload = ZKModelFormat.load_model(file_path)
            return payload, {"metadata": metadata}
        elif fmt == ModelFormat.PYTORCH:
            state_dict = torch.load(file_path, map_location=device)
            return state_dict, {}
        elif fmt == ModelFormat.SAFETENSORS:
            try:
                from safetensors.torch import load_file
                return load_file(file_path, device=device), {}
            except ImportError:
                raise ModelError("safetensors library required to load .safetensors files")

        raise ModelError(f"Unsupported model container format: {fmt.value}")
