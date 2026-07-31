"""Custom Exception Hierarchy for ZKAI."""

from typing import Optional, Any, Dict


class ZKAIError(Exception):
    """Base exception class for all ZKAI framework errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, details={self.details!r})"


class BackendError(ZKAIError):
    """Raised when an underlying backend (e.g. PyTorch, CUDA) operation fails."""
    pass


class ConfigError(ZKAIError):
    """Raised when configuration validation or initialization fails."""
    pass


class NeuralError(ZKAIError):
    """Raised during neural network operations, forward/backward pass, or layer mismatch."""
    pass


class ModelError(ZKAIError):
    """Raised when model loading, saving, serialization or conversion fails."""
    pass


class InferenceError(ZKAIError):
    """Raised during generation, sampling, or token processing in inference."""
    pass


class TrainingError(ZKAIError):
    """Raised during training, gradient calculation, or optimization failure."""
    pass


class MemoryError(ZKAIError):
    """Raised when memory storage, retrieval, consolidation, or indexing fails."""
    pass


class AgentError(ZKAIError):
    """Raised when agent planning, execution, reflection, or retry fails."""
    pass


class ToolError(ZKAIError):
    """Raised during tool execution, parameter resolution, or permission check."""
    pass


class VisionError(ZKAIError):
    """Raised during image, video, OCR, or camera processing."""
    pass


class AudioError(ZKAIError):
    """Raised during speech-to-text, text-to-speech, or audio recording."""
    pass


class DocumentError(ZKAIError):
    """Raised during document loading, parsing, chunking, or indexing."""
    pass


class CodingError(ZKAIError):
    """Raised during code execution, linting, debugging, or sandboxing."""
    pass


class ComputerError(ZKAIError):
    """Raised during screen capture, mouse/keyboard automation, or UI detection."""
    pass


class InternetError(ZKAIError):
    """Raised during web searching, crawling, scraping, or fact verification."""
    pass


class BrowserError(ZKAIError):
    """Raised during headless browser interactions or Playwright operations."""
    pass


class DatabaseError(ZKAIError):
    """Raised during database connection, query, or storage operations."""
    pass


class PluginError(ZKAIError):
    """Raised during plugin loading, registration, or execution."""
    pass


class SerializationError(ZKAIError):
    """Raised during .zk format parsing or data serialization/deserialization."""
    pass


class EvaluationError(ZKAIError):
    """Raised during critic, verifier, or self-reflection pipeline execution."""
    pass


class TokenizerError(ZKAIError):
    """Raised during tokenization encoding, decoding, or vocabulary training."""
    pass


class DatasetError(ZKAIError):
    """Raised during dataset loading, sampling, collation, or transform application."""
    pass


class QuantizationError(ZKAIError):
    """Raised during weight quantization, packing, or export operations."""
    pass


class SecurityError(ZKAIError):
    """Raised during secret access, encrypted storage, or permission evaluation."""
    pass


class KnowledgeError(ZKAIError):
    """Raised during knowledge base store, search, or revision control operations."""
    pass


class HubError(ZKAIError):
    """Raised during model hub download, upload, or version resolution."""
    pass


class BenchmarkError(ZKAIError):
    """Raised during benchmark suite execution or metric evaluation."""
    pass


class ReasoningError(ZKAIError):
    """Raised during tree search, graph reasoning, or consensus evaluation."""
    pass


class RoboticsError(ZKAIError):
    """Raised during sensor capture, GPIO control, or ROS bridge communication."""
    pass


class GraphCompilerError(ZKAIError):
    """Raised during computation graph compilation, fusion, or planning."""
    pass


class StorageError(ZKAIError):
    """Raised during storage provider, object store, or blob store operations."""
    pass


class EmbeddingError(ZKAIError):
    """Raised during embedding generation, cross-modal alignment, or indexing."""
    pass


class WorkflowError(ZKAIError):
    """Raised during DAG workflow node execution, routing, or scheduling."""
    pass


class ConverterError(ZKAIError):
    """Raised during universal model weights format conversion or validation."""
    pass


class ClusterError(ZKAIError):
    """Raised during distributed inference cluster allocation, routing, or failover."""
    pass


class EvalError(ZKAIError):
    """Raised during LLM benchmark evaluation suite execution or report generation."""
    pass


class KernelError(ZKAIError):
    """Raised during AI Kernel runtime, scheduling, or lifecycle operations."""
    pass


