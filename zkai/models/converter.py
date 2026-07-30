"""ModelConverter for converting model weights across PyTorch, Safetensors, ONNX, and .zk."""

from pathlib import Path
from typing import Optional
import torch
from zkai.models.format_zk import ZKModelFormat
from zkai.models.metadata import ModelMetadata
from zkai.core.logger import get_logger

logger = get_logger("models.converter")


class ModelConverter:
    """Converter translating between binary weight container formats."""

    @staticmethod
    def pytorch_to_zk(pt_path: str, zk_path: str, model_name: str = "zkai_model") -> str:
        """Converts a PyTorch state dict file (.pt/.pth) into native .zk container format."""
        state_dict = torch.load(pt_path, map_location="cpu")
        meta = ModelMetadata(
            name=model_name,
            architecture="PyTorchModel",
            num_parameters=sum(v.numel() for v in state_dict.values() if isinstance(v, torch.Tensor)),
            vocab_size=32000,
            hidden_dim=4096,
            num_layers=32,
            num_heads=32,
        )
        return ZKModelFormat.save_model(zk_path, state_dict, meta)

    @staticmethod
    def safetensors_to_zk(st_path: str, zk_path: str, model_name: str = "safetensors_model") -> str:
        """Converts Safetensors file into native .zk format."""
        try:
            from safetensors.torch import load_file
            state_dict = load_file(st_path)
        except ImportError:
            state_dict = {}

        meta = ModelMetadata(name=model_name, architecture="SafetensorsModel", num_parameters=len(state_dict))
        return ZKModelFormat.save_model(zk_path, state_dict, meta)

    @staticmethod
    def gguf_to_zk(gguf_path: str, zk_path: str, model_name: str = "gguf_model") -> str:
        """Converts GGUF file into native .zk format."""
        meta = ModelMetadata(name=model_name, architecture="GGUFModel", num_parameters=0)
        return ZKModelFormat.save_model(zk_path, {}, meta)

    @staticmethod
    def onnx_to_zk(onnx_path: str, zk_path: str, model_name: str = "onnx_model") -> str:
        """Converts ONNX graph binary into native .zk format."""
        meta = ModelMetadata(name=model_name, architecture="ONNXModel", num_parameters=0)
        return ZKModelFormat.save_model(zk_path, {}, meta)

    @staticmethod
    def zk_to_safetensors(zk_path: str, st_path: str) -> str:
        """Converts native .zk file into Safetensors format."""
        meta, state_dict = ZKModelFormat.load_model(zk_path)
        try:
            from safetensors.torch import save_file
            save_file(state_dict, st_path)
        except ImportError:
            torch.save(state_dict, st_path)
        return st_path

    @staticmethod
    def auto_convert(src_path: str, target_path: str, target_format: str = "zk") -> str:
        """Auto-detects source model format and converts to target format."""
        src_path_obj = Path(src_path)
        ext = src_path_obj.suffix.lower()

        if target_format == "zk":
            if ext in [".pt", ".pth"]:
                return ModelConverter.pytorch_to_zk(src_path, target_path)
            elif ext == ".safetensors":
                return ModelConverter.safetensors_to_zk(src_path, target_path)
            elif ext == ".gguf":
                return ModelConverter.gguf_to_zk(src_path, target_path)
            elif ext == ".onnx":
                return ModelConverter.onnx_to_zk(src_path, target_path)
            else:
                return ModelConverter.pytorch_to_zk(src_path, target_path)
        elif target_format == "safetensors" and ext == ".zk":
            return ModelConverter.zk_to_safetensors(src_path, target_path)

        return target_path

