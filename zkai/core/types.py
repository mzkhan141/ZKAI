"""Shared type definitions, enums, protocols, and type aliases for ZKAI."""

from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union
import sys


class DeviceType(str, Enum):
    """Supported computation devices."""
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"
    AUTO = "auto"


class DType(str, Enum):
    """Supported data precision types."""
    FLOAT32 = "float32"
    FLOAT16 = "float16"
    BFLOAT16 = "bfloat16"
    INT8 = "int8"
    INT4 = "int4"
    INT32 = "int32"
    INT64 = "int64"
    BOOL = "bool"


class BackendType(str, Enum):
    """Supported backend engines."""
    PYTORCH = "pytorch"
    JAX = "jax"
    TINYGRAD = "tinygrad"
    CUSTOM = "custom"


class MemoryType(str, Enum):
    """Supported memory taxonomy types."""
    WORKING = "working"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    ENTITY = "entity"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    VECTOR = "vector"
    EMBEDDING = "embedding"
    FILE = "file"
    CODE = "code"
    COMPRESSED = "compressed"
    ARCHIVED = "archived"


class TaskStatus(str, Enum):
    """Status of asynchronous tasks."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class Priority(int, Enum):
    """Priority levels for task scheduling and queues."""
    LOW = 0
    MEDIUM = 5
    HIGH = 10
    CRITICAL = 20


class ModelFormat(str, Enum):
    """Supported model file formats."""
    ZK = "zk"
    PYTORCH = "pytorch"
    SAFETENSORS = "safetensors"
    GGUF = "gguf"
    GGML = "ggml"
    ONNX = "onnx"
    HUGGINGFACE = "huggingface"
    TENSORRT = "tensorrt"
    OPENVINO = "openvino"
    MLX = "mlx"


class WorkflowNodeType(str, Enum):
    """Supported node execution types in DAG workflow engine."""
    ACTION = "action"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PARALLEL = "parallel"
    MERGE = "merge"
    RETRY = "retry"
    HUMAN_APPROVAL = "human_approval"


class StorageBackendType(str, Enum):
    """Supported storage provider backends."""
    SQLITE = "sqlite"
    DUCKDB = "duckdb"
    LMDB = "lmdb"
    REDIS = "redis"
    BLOB = "blob"
    OBJECT = "object"
    CACHE = "cache"
    SESSION = "session"
    AUTO = "auto"


class EmbeddingModalityType(str, Enum):
    """Modality types supported by embedding framework."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    CROSS_MODAL = "cross_modal"


class Role(str, Enum):
    """Roles in conversation and prompts."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"


class DocumentType(str, Enum):
    """Multimodal document types."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"
    DOCX = "docx"
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"


# Generic type aliases
TensorData = Any
ArrayLike = Union[List[float], List[int], List[Any], Tuple[Any, ...]]
Shape = Tuple[int, ...]
MetadataDict = Dict[str, Any]
JsonDict = Dict[str, Any]

