"""HuggingFaceCompat wrapper allowing loading HF models without hard dependency."""

from typing import Any, Dict, Optional
from zkai.core.logger import get_logger

logger = get_logger("compat.huggingface")

try:
    import transformers
except ImportError:
    transformers = None


class HuggingFaceCompat:
    """HuggingFace Transformers compatibility adapter."""

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir

    def load_hf_tokenizer(self, model_name_or_path: str) -> Any:
        if not transformers:
            logger.warning("transformers library not installed; HF tokenizer load fallback.")
            return None
        try:
            return transformers.AutoTokenizer.from_pretrained(model_name_or_path, cache_dir=self.cache_dir)
        except Exception as e:
            logger.warning(f"Could not load HF tokenizer '{model_name_or_path}': {e}")
            return None

    def load_hf_model(self, model_name_or_path: str) -> Any:
        if not transformers:
            logger.warning("transformers library not installed; HF model load fallback.")
            return None
        try:
            return transformers.AutoModelForCausalLM.from_pretrained(model_name_or_path, cache_dir=self.cache_dir)
        except Exception as e:
            logger.warning(f"Could not load HF model '{model_name_or_path}': {e}")
            return None
