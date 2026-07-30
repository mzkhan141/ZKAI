"""ONNXCompat wrapper for executing ONNX models without architectural dependency."""

from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("compat.onnx")

try:
    import onnxruntime as ort
except ImportError:
    ort = None


class ONNXCompat:
    """ONNX Runtime execution wrapper."""

    def __init__(self, onnx_model_path: str, provider: str = "CPUExecutionProvider"):
        self.path = onnx_model_path
        self.session = ort.InferenceSession(onnx_model_path, providers=[provider]) if ort else None

    def run_inference(self, input_feed: Dict[str, Any]) -> List[Any]:
        if not self.session:
            logger.warning("onnxruntime library not installed; returning mock output.")
            return []
        output_names = [o.name for o in self.session.get_outputs()]
        return self.session.run(output_names, input_feed)
