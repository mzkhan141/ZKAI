"""Hierarchical Configuration System for ZKAI built with Pydantic."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from zkai.core.types import DeviceType, DType, BackendType


class NeuralConfig(BaseModel):
    """Configuration for neural computation and layer defaults."""
    default_dtype: DType = DType.FLOAT32
    device: DeviceType = DeviceType.AUTO
    enable_cuda_graphs: bool = True
    seed: int = 42


class TransformerConfig(BaseModel):
    """Configuration for modern Transformer architectures."""
    vocab_size: int = 32000
    hidden_dim: int = 4096
    num_layers: int = 32
    num_heads: int = 32
    num_kv_heads: Optional[int] = None  # Grouped Query Attention if set (must be <= num_heads)
    head_dim: int = 128
    intermediate_dim: int = 11008
    max_position_embeddings: int = 4096
    rope_theta: float = 10000.0
    use_alibi: bool = False
    use_flash_attention: bool = True
    dropout: float = 0.0
    layer_norm_eps: float = 1e-5
    num_experts: int = 0  # MoE if > 0
    num_experts_per_tok: int = 0


class MemoryConfig(BaseModel):
    """Configuration for all 14 ZKAI memory subsystems."""
    working_memory_capacity: int = 20
    short_term_capacity: int = 1000
    vector_dimension: int = 384
    similarity_threshold: float = 0.75
    enable_consolidation: bool = True
    decay_rate: float = 0.05
    persistence_dir: str = "./memory_store"


class VisionConfig(BaseModel):
    """Configuration for vision processing and multimodal capabilities."""
    image_size: int = 224
    ocr_languages: List[str] = Field(default_factory=lambda: ["en"])
    camera_device_id: int = 0
    confidence_threshold: float = 0.5


class AudioConfig(BaseModel):
    """Configuration for speech-to-text, text-to-speech, and VAD."""
    stt_model: str = "base"
    tts_voice: str = "default"
    sample_rate: int = 16000
    vad_threshold: float = 0.5


class BrowserConfig(BaseModel):
    """Configuration for browser automation and scraping."""
    headless: bool = True
    user_agent: str = "ZKAI-BrowserAgent/1.0"
    timeout: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720


class InternetConfig(BaseModel):
    """Configuration for internet search, crawling, and verification."""
    max_search_results: int = 10
    credibility_threshold: float = 0.6
    enable_fact_checking: bool = True
    user_agent: str = "ZKAI-SearchAgent/1.0"


class ComputerConfig(BaseModel):
    """Configuration for screen interaction and OS automation."""
    display_index: int = 0
    mouse_move_duration: float = 0.2
    ocr_confidence: float = 0.6


class CodingConfig(BaseModel):
    """Configuration for sandboxed code execution."""
    execution_timeout: int = 30
    use_docker: bool = False
    sandbox_dir: str = "./zkai_sandbox"


class AgentConfig(BaseModel):
    """Configuration for agent reasoning, planning, and self-evaluation."""
    max_iterations: int = 15
    confidence_threshold: float = 0.8
    enable_reflection: bool = True
    enable_verification: bool = True
    retry_attempts: int = 3


class TrainingConfig(BaseModel):
    """Configuration for model training and fine-tuning."""
    batch_size: int = 32
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    warmup_steps: int = 1000
    max_steps: int = 100000
    gradient_accumulation_steps: int = 1
    mixed_precision: DType = DType.FLOAT16
    checkpoint_interval: int = 1000
    output_dir: str = "./checkpoints"


class TokenizerConfig(BaseModel):
    """Configuration for native tokenizer subsystem."""
    tokenizer_type: str = "bpe"
    vocab_size: int = 32000
    special_tokens: List[str] = Field(default_factory=lambda: ["<pad>", "<unk>", "<s>", "</s>", "<mask>"])


class DatasetConfig(BaseModel):
    """Configuration for dataset loading and processing."""
    num_workers: int = 4
    prefetch_factor: int = 2
    pin_memory: bool = True
    cache_dir: str = "./dataset_cache"


class DistributedConfig(BaseModel):
    """Configuration for distributed training."""
    strategy: str = "ddp"
    num_nodes: int = 1
    gpus_per_node: int = 1
    backend: str = "nccl"


class PEFTConfig(BaseModel):
    """Configuration for Parameter-Efficient Fine-Tuning."""
    method: str = "lora"
    lora_rank: int = 16
    lora_alpha: float = 32.0
    target_modules: List[str] = Field(default_factory=lambda: ["q_proj", "v_proj"])


class QuantizationConfig(BaseModel):
    """Configuration for model weight quantization."""
    bits: int = 8
    method: str = "weight_only"
    group_size: int = 128


class SecurityConfig(BaseModel):
    """Configuration for security and access control."""
    enable_audit: bool = True
    secret_key_env: str = "ZKAI_SECRET_KEY"
    sandbox_enabled: bool = True


class KnowledgeConfig(BaseModel):
    """Configuration for knowledge base management."""
    storage_dir: str = "./knowledge_store"
    embedding_model: str = "default"
    search_top_k: int = 5


class HubConfig(BaseModel):
    """Configuration for model hub interaction."""
    cache_dir: str = "./hub_cache"
    default_repository: str = "zkai-models"


class BenchmarkConfig(BaseModel):
    """Configuration for benchmark suite execution."""
    iterations: int = 50
    warmup_iterations: int = 5
    report_format: str = "markdown"


class RoboticsConfig(BaseModel):
    """Configuration for robotics hardware interface."""
    camera_id: int = 0
    serial_port: str = "COM3"
    baudrate: int = 115200


class InferenceConfig(BaseModel):
    """Configuration for high-performance continuous batching inference engine."""
    max_batch_size: int = 32
    max_sequence_len: int = 4096
    enable_continuous_batching: bool = True
    enable_speculative_decoding: bool = False
    draft_model_path: Optional[str] = None
    block_size: int = 16
    gpu_memory_utilization: float = 0.90


class GraphCompilerConfig(BaseModel):
    """Configuration for computation graph compiler and optimizer."""
    opt_level: int = 2
    enable_fusion: bool = True
    enable_constant_folding: bool = True
    enable_dead_code_elimination: bool = True
    device_target: str = "auto"


class StorageConfig(BaseModel):
    """Configuration for unified storage framework."""
    default_backend: str = "auto"
    sqlite_path: str = "zkai_storage.db"
    duckdb_path: str = "zkai_analytics.duckdb"
    lmdb_path: str = "./zkai_lmdb"
    redis_url: str = "redis://localhost:6379/0"
    blob_dir: str = "./blob_store"


class EmbeddingConfig(BaseModel):
    """Configuration for embedding models and similarity indices."""
    default_dimension: int = 384
    text_model: str = "all-MiniLM-L6-v2"
    device: str = "auto"
    batch_size: int = 64
    metric: str = "cosine"


class WorkflowConfig(BaseModel):
    """Configuration for DAG workflow execution engine."""
    max_concurrent_nodes: int = 8
    default_retry_count: int = 3
    timeout_seconds: int = 300
    enable_human_approval: bool = True


class ClusterConfig(BaseModel):
    """Configuration for distributed inference clusters."""
    cluster_name: str = "zkai-cluster"
    num_replicas: int = 1
    gpus_per_replica: int = 1
    load_balancing_policy: str = "round_robin"
    network_transport: str = "simulated"
    single_gpu_mode: bool = True


class LLMEvalConfig(BaseModel):
    """Configuration for benchmark suites."""
    eval_batch_size: int = 16
    output_dir: str = "./eval_reports"
    benchmarks: List[str] = Field(default_factory=lambda: ["mmlu", "gsm8k", "humaneval", "arc", "truthfulqa", "bbh", "hellaswag", "agentbench"])


class CompatConfig(BaseModel):
    """Configuration for ecosystem compatibility layers."""
    hf_cache_dir: Optional[str] = None
    onnx_execution_provider: str = "CPUExecutionProvider"
    tensorrt_workspace_size: int = 1 << 30


class BootConfig(BaseModel):
    """Configuration for Boot Loader and state machine."""
    profile: str = "full"
    safe_mode: bool = False
    recovery_mode: bool = False
    timeout_seconds: float = 30.0


class GovernanceConfig(BaseModel):
    """Configuration for Resource Governor quotas and rate limits."""
    cpu_limit: float = 8.0
    gpu_limit: float = 1.0
    vram_mb_limit: float = 8192.0
    ram_mb_limit: float = 16384.0
    rate_limit_per_sec: float = 50.0


class SnapshotConfig(BaseModel):
    """Configuration for system snapshot persistence and WAL recovery journal."""
    auto_snapshot: bool = True
    interval_seconds: float = 300.0
    storage_dir: str = "./snapshots"


class ObservabilityConfig(BaseModel):
    """Configuration for enterprise observability and distributed tracing."""
    enable_tracing: bool = True
    enable_metrics: bool = True
    enable_crash_reporting: bool = True


class TenantConfig(BaseModel):
    """Configuration for multi-tenant isolation and security."""
    default_tier: str = "personal"
    workspace_isolation: bool = True


class ZKAIConfig(BaseModel):
    """Top-level master configuration for the ZKAI AI Operating System."""
    device: DeviceType = DeviceType.AUTO
    dtype: DType = DType.FLOAT32
    backend: BackendType = BackendType.PYTORCH
    memory_limit: str = "24GB"
    reasoning: bool = True
    vision: bool = True
    audio: bool = True
    browser: bool = True
    internet: bool = True
    computer: bool = True
    coding: bool = True

    neural: NeuralConfig = Field(default_factory=NeuralConfig)
    transformer: TransformerConfig = Field(default_factory=TransformerConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    vision_cfg: VisionConfig = Field(default_factory=VisionConfig)
    audio_cfg: AudioConfig = Field(default_factory=AudioConfig)
    browser_cfg: BrowserConfig = Field(default_factory=BrowserConfig)
    internet_cfg: InternetConfig = Field(default_factory=InternetConfig)
    computer_cfg: ComputerConfig = Field(default_factory=ComputerConfig)
    coding_cfg: CodingConfig = Field(default_factory=CodingConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    tokenizer: TokenizerConfig = Field(default_factory=TokenizerConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    distributed: DistributedConfig = Field(default_factory=DistributedConfig)
    peft: PEFTConfig = Field(default_factory=PEFTConfig)
    quantization: QuantizationConfig = Field(default_factory=QuantizationConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    knowledge: KnowledgeConfig = Field(default_factory=KnowledgeConfig)
    hub: HubConfig = Field(default_factory=HubConfig)
    benchmark: BenchmarkConfig = Field(default_factory=BenchmarkConfig)
    robotics: RoboticsConfig = Field(default_factory=RoboticsConfig)
    inference: InferenceConfig = Field(default_factory=InferenceConfig)
    graph_compiler: GraphCompilerConfig = Field(default_factory=GraphCompilerConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)
    cluster: ClusterConfig = Field(default_factory=ClusterConfig)
    llm_eval: LLMEvalConfig = Field(default_factory=LLMEvalConfig)
    compat: CompatConfig = Field(default_factory=CompatConfig)
    boot: BootConfig = Field(default_factory=BootConfig)
    governance: GovernanceConfig = Field(default_factory=GovernanceConfig)
    snapshot: SnapshotConfig = Field(default_factory=SnapshotConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    tenant: TenantConfig = Field(default_factory=TenantConfig)


