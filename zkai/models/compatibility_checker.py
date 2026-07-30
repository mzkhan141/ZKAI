"""CompatibilityChecker verifying model format conversion support and operator compatibility."""

from typing import Dict, List, Tuple
from zkai.core.types import ModelFormat
from zkai.core.exceptions import ConverterError
from zkai.core.logger import get_logger

logger = get_logger("models.compatibility_checker")


class CompatibilityChecker:
    """Validates compatibility between source and target model weight container formats."""

    SUPPORTED_CONVERSIONS: Dict[ModelFormat, List[ModelFormat]] = {
        ModelFormat.PYTORCH: [ModelFormat.ZK, ModelFormat.SAFETENSORS, ModelFormat.ONNX, ModelFormat.GGUF, ModelFormat.TENSORRT],
        ModelFormat.SAFETENSORS: [ModelFormat.ZK, ModelFormat.PYTORCH, ModelFormat.GGUF, ModelFormat.ONNX],
        ModelFormat.GGUF: [ModelFormat.ZK, ModelFormat.PYTORCH, ModelFormat.GGML],
        ModelFormat.GGML: [ModelFormat.ZK, ModelFormat.GGUF],
        ModelFormat.ONNX: [ModelFormat.ZK, ModelFormat.TENSORRT, ModelFormat.OPENVINO],
        ModelFormat.ZK: [ModelFormat.PYTORCH, ModelFormat.SAFETENSORS, ModelFormat.ONNX, ModelFormat.GGUF],
    }

    def check_compatibility(self, src_format: ModelFormat, tgt_format: ModelFormat) -> bool:
        """Returns True if direct conversion path exists between formats."""
        allowed = self.SUPPORTED_CONVERSIONS.get(src_format, [])
        return tgt_format in allowed

    def validate_or_raise(self, src_format: ModelFormat, tgt_format: ModelFormat) -> None:
        """Raises ConverterError if conversion is unsupported."""
        if not self.check_compatibility(src_format, tgt_format):
            raise ConverterError(f"Conversion from '{src_format.value}' to '{tgt_format.value}' is not supported.")
