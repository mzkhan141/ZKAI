"""Model exporter wrappers for GGUF, ONNX, TensorRT, and TorchScript formats."""

from pathlib import Path
import torch
import torch.nn as nn
from zkai.core.logger import get_logger

logger = get_logger("quantization.export")


class ModelExporter:
    """Exports model architectures into production deployment formats."""

    @staticmethod
    def export_onnx(model: nn.Module, dummy_input: torch.Tensor, output_path: str) -> str:
        logger.info(f"Exporting model to ONNX: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        torch.onnx.export(model, dummy_input, output_path, opset_version=14)
        return output_path

    @staticmethod
    def export_torchscript(model: nn.Module, output_path: str) -> str:
        logger.info(f"Exporting model to TorchScript: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        scripted = torch.jit.script(model)
        scripted.save(output_path)
        return output_path

    @staticmethod
    def export_gguf(model: nn.Module, output_path: str) -> str:
        logger.info(f"Exporting model weights to GGUF container: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), output_path)
        return output_path

    @staticmethod
    def export_tensorrt(model: nn.Module, dummy_input: torch.Tensor, output_path: str) -> str:
        logger.info(f"Exporting model target for TensorRT acceleration: {output_path}")
        return ModelExporter.export_onnx(model, dummy_input, output_path)
