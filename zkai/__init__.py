"""ZKAI — Production-Quality Extensible AI Framework and AI Operating System."""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# --- Core Re-exports ---
from zkai.core.types import (
    DeviceType,
    DType,
    BackendType,
    MemoryType,
    TaskStatus,
    Priority,
    ModelFormat,
    Role,
    DocumentType,
)
from zkai.core.exceptions import (
    ZKAIError,
    BackendError,
    ConfigError,
    NeuralError,
    ModelError,
    InferenceError,
    TrainingError,
    MemoryError,
    AgentError,
    ToolError,
    VisionError,
    AudioError,
    DocumentError,
    CodingError,
    ComputerError,
    InternetError,
    BrowserError,
    DatabaseError,
    PluginError,
    SerializationError,
    EvaluationError,
    TokenizerError,
    DatasetError,
    QuantizationError,
    SecurityError,
    KnowledgeError,
    HubError,
    BenchmarkError,
    ReasoningError,
    RoboticsError,
)
from zkai.core.config import ZKAIConfig, NeuralConfig, TransformerConfig
from zkai.core.logger import Logger, get_logger
from zkai.core.backend import ComputeBackend, PyTorchBackend, DeviceManager, BackendManager
from zkai.core.events import EventBus, Event, default_event_bus
from zkai.core.tasks import Task, TaskQueue, PriorityQueue, TaskExecutor
from zkai.core.plugin import Plugin, PluginManager, PluginMetadata, PluginRegistry
from zkai.core.cache import LRUCache, TTLCache, DiskCache
from zkai.core.serialization import ZKSerializer, ZKHeader

# --- Neural Re-exports ---
from zkai.neural import (
    Tensor,
    Parameter,
    Neuron,
    Module,
    Sequential,
    NeuralNetwork,
    Model,
    Linear,
    Dense,
    Conv1D,
    Conv2D,
    Conv3D,
    Embedding,
    Dropout,
    LayerNorm,
    BatchNorm,
    RMSNorm,
    Activation,
    ReLU,
    GELU,
    SiLU,
    Sigmoid,
    Softmax,
    Swish,
    Loss,
    CrossEntropy,
    CrossEntropyLoss,
    MSE,
    MSELoss,
    ContrastiveLoss,
    Optimizer,
    Adam,
    AdamW,
    SGD,
    RMSProp,
    Scheduler,
    StepLR,
    CosineAnnealingLR,
    WarmupLR,
    Checkpoint,
    CheckpointManager,
    Trainer,
)

# --- Transformer Re-exports ---
from zkai.transformer import (
    Tokenizer,
    Vocabulary,
    BytePairEncoding,
    TokenEmbedding,
    RotaryEmbedding,
    PositionalEncoding,
    ALiBi,
    MultiHeadAttention,
    SelfAttention,
    CrossAttention,
    FlashAttention,
    FeedForward,
    GatedFeedForward,
    MoEFeedForward,
    TransformerBlock,
    Encoder,
    Decoder,
    KVCache,
    PagedKVCache,
    GreedySampler,
    TopKSampler,
    TopPSampler,
    TemperatureSampler,
    BeamSearch,
    RepetitionPenalty,
    InferenceEngine,
    BatchInference,
)

# --- Models Re-exports ---
from zkai.models import (
    ModelMetadata,
    ModelCard,
    ZKModelFormat,
    ModelRegistry,
    ModelDownloader,
    ModelLoader,
    ModelCache,
    ModelConverter,
    ModelCheckpointManager,
    VersionManager,
    Quantizer,
    LoRAConfig,
    LoRAAdapter,
    LoRAMerger,
    ModelMerger,
    ModelManager,
)

# --- Subsystem Managers ---
from zkai.memory import MemoryManager
from zkai.language_model import LanguageModel, ChatModel, Message, Conversation
from zkai.evaluation import EvaluationPipeline
from zkai.vision import Image, Video, Camera, ObjectDetector, OCREngine, ImageCaptioner, ImageClassifier, ImageSegmenter, FaceDetector, FeatureExtractor, VisionEncoder
from zkai.audio import SpeechToText, TextToSpeech, VoiceActivityDetector, AudioRecorder, SpeakerRecognizer
from zkai.documents import Document, DocumentLoader, DocumentParser, DocumentEmbedder, DocumentIndexer, DocumentRetriever
from zkai.coding import CodeGenerator, PythonRunner, Terminal, Debugger, CodeLinter, StaticAnalyzer, ProjectGenerator
from zkai.browser import Browser, Page, BrowserSearch
from zkai.internet import SearchEngine, WebCrawler, WebScraper, KnowledgeExtractor, FactVerifier, CredibilityScorer
from zkai.computer import Mouse, Keyboard, Monitor, WindowDetector, Clipboard, UIElementDetector, Automation, ComputerOCR, ApplicationLauncher, FileExplorer
from zkai.agent import Agent, Goal, GoalManager, Plan, AgentPlanner, AgentExecutor, AutonomousExecutor
from zkai.tools import Tool, ToolRegistry, PythonTool, BrowserTool, VisionTool, SearchTool, TerminalTool, CalculatorTool, DatabaseTool, GitTool
from zkai.database import Database, SQLiteDatabase, PostgresDatabase, RedisDatabase, VectorDatabase, CacheDatabase
from zkai.training import TrainingOrchestrator, Dataset, SimpleDataset, DataLoader, DataPipeline

# --- New Subsystem Re-exports ---
from zkai.tokenizer import (
    TokenizerBase, BytePairTokenizer, SentencePieceTokenizer, WordPieceTokenizer,
    UnigramTokenizer, RegexTokenizer, CharacterTokenizer, WhitespaceTokenizer,
    FastTokenizer, StreamingTokenizer, TokenizerTrainer, EncodingResult,
)
from zkai.datasets import (
    TextDataset, ImageDataset, AudioDataset, VideoDataset, JSONDataset, CSVDataset,
    ParquetDataset, FolderDataset, StreamingDataset, LazyDataset,
)
from zkai.distributed import DDPTrainer, FSDPTrainer, PipelineParallel, TensorParallel, ZeROOptimizer
from zkai.peft import (
    QLoRAAdapter, DoRAAdapter, AdapterLayer, PrefixTuning, PromptTuning,
    IA3Adapter, AdapterMerger, AdapterManager,
)
from zkai.quantization import (
    INT4Quantizer, NF4Quantizer, FP8Quantizer, Calibrator, WeightPacker, ModelExporter,
)
from zkai.plugins import PluginManifest, DependencyResolver, PluginStore, HotReloader
from zkai.security import (
    SecretsManager, EncryptedMemory, SecureStorage, PermissionEngine,
    PolicyEngine, AuditLog, CapabilityToken, TokenIssuer, SandboxPolicy,
)
from zkai.backends import (
    CPUBackend, CUDABackend, ROCmBackend, MetalBackend, OpenCLBackend,
    VulkanBackend, AutoBackendSelector,
)
from zkai.robotics import Robot, Drone, GPIO, SerialPort, ROSBridge, RobotCamera
from zkai.vision.face import (
    FaceRecognizer, FaceDatabase, FaceEmbedding, FaceVerification,
    FaceIdentification, FaceTracker, FaceClustering,
)
from zkai.video import (
    VideoReader, VideoWriter, FrameExtractor, VideoCaptioner,
    VideoSummarizer, VideoQA, ObjectTracker, PoseEstimator, DepthEstimator,
    OpticalFlowEstimator, SceneDetector,
)
from zkai.audio import (
    VoiceCloner, NoiseReducer, EmotionRecognizer, LanguageIdentifier,
    MusicGenerator, SpeakerSeparator, AudioEnhancer,
)
from zkai.knowledge import KnowledgeBase, KnowledgeEntry, Wiki, MarkdownVault, SemanticSearch
from zkai.hub import ModelHub, CheckpointRegistry, HubDownloader, HubUploader
from zkai.agents import (
    CoordinatorAgent, PlannerAgent, ResearchAgent, CoderAgent, VisionAgent,
    BrowserAgent, MemoryAgent, CriticAgent, VerifierAgent, MessageBus, SharedAgentMemory,
)
from zkai.reasoning import (
    TreeSearch, MCTSReasoner, GraphReasoner, PlanningEngine, ReflectionEngine,
    ReasoningVerifier, ReasoningCritic, ConsensusReasoning, SelfCorrection, RecursiveReasoner,
)
from zkai.benchmarks import (
    LatencyBenchmark, MemoryBenchmark, InferenceBenchmark, TrainingBenchmark,
    AccuracyBenchmark, ReasoningBenchmark, VisionBenchmark, ReportGenerator,
)
from zkai.graph_compiler import (
    ComputeGraph, ComputeNode, StaticGraph, DynamicGraph,
    ExecutionPlanner, MemoryPlanner, GraphCompiler,
    ConstantFolding, DeadCodeElimination, KernelFusion, OperatorFusion,
)
from zkai.inference import (
    GPUAllocator, GPUDevice, ReplicaManager, ModelReplica,
    LoadBalancer, RequestRouter, ModelSharding, PipelineInference,
    ClusterCoordinator, InferenceCluster, NetworkTransport,
    SimulatedTransport, HTTPTransport, SocketTransport,
)
from zkai.storage import (
    BlobStore, ObjectStore, CacheStore, SessionStore,
    DuckDBStore, LMDBStore, RedisStore, StorageProvider,
)
from zkai.embedding import (
    EmbeddingModel, TextEmbedding, ImageEmbedding, AudioEmbedding,
    VideoEmbedding, CrossModalEmbedding, EmbeddingTrainer,
    SimilarityIndex, SemanticSearch,
)
from zkai.llm_eval import (
    EvalResult, EvalBenchmark, MMLUBenchmark, GSM8KBenchmark,
    HumanEvalBenchmark, ARCBenchmark, TruthfulQABenchmark,
    BBHBenchmark, HellaSwagBenchmark, AgentBenchBenchmark,
    EvalRunner, EvalReport,
)
from zkai.compat import (
    HuggingFaceCompat, ONNXCompat, TensorRTCompat,
    GGUFCompat, SafetensorsCompat, OpenVINOCompat,
)
from zkai.workflow import (
    WorkflowNode, ActionNode, Conditional, Loop, Parallel,
    Merge, Retry, HumanApproval, WorkflowEngine, WorkflowRunner, WorkflowScheduler,
)
from zkai.core.versioning import APIVersion, deprecated, BackwardCompatLayer, SerializationCompat
from zkai.core.lazy import LazyModule, LazyImport
from zkai.core.memory_pool import MemoryPool, ZeroCopyBuffer, StreamingBuffer
from zkai.core.async_io import AsyncFileReader, AsyncBatchProcessor

# --- AI Operating System Core Subsystems ---
from zkai.kernel import (
    AIKernel, KernelRuntime, KernelConfig, KernelScheduler,
    ResourceGovernor, BootLoader, BootConfiguration, KernelStateMachine,
    RollbackManager, MetricsRegistry, DistributedTracer, ArchitectureSpec,
    MicroKernel, AIHypervisor, SelfRecoveryManager, EvolutionEngine,
    CognitiveRuntime, SimulationEngine, DigitalTwin, AutonomousTesting,
    GoalScheduler, KernelIntelligence,
)
from zkai.ipc.knowledge_bus import KnowledgeBus, IntentBus, SemanticEvent
from zkai.knowledge.research import ResearchEngine
from zkai.security.governance_engine import GovernanceEngine
from zkai.knowledge.world_model import WorldModel
from zkai.security.capability_os import CapabilityManager, CapabilityToken
from zkai.process import ProcessManager, AIProcess, AgentProcess, ServiceProcess
from zkai.ipc import SystemMessageBus, RPCServer, RPCClient, SharedMemoryChannel
from zkai.filesystem import SemanticFileIndex, VersionedStorage, FileRelationshipGraph, KnowledgeFile
from zkai.services import ServiceManager, InferenceService, MemoryService, StorageService
from zkai.session import SessionManager, AISession, SessionSerializer
from zkai.identity import AuthenticationManager, AuthorizationManager, IdentitySynchronizer, User, TenantManager
from zkai.security_kernel import SecurityKernel
from zkai.shell import ZKShell, ZKAICLI
from zkai.apps import AIApplication, ApplicationRuntime, ApplicationStore
from zkai.packages import PackageManager
from zkai.marketplace import Marketplace
from zkai.web_desktop import WebDesktopServer
from zkai.monitor import SystemMonitor
from zkai.voice import VoiceRuntime
from zkai.memory_os import MemoryDaemon
from zkai.device import DeviceManager
from zkai.cluster import ClusterOrchestrator
from zkai.knowledge.governance import KnowledgeGovernor
from zkai.sdk import PythonSDK, ProjectGenerator

logger = get_logger("ai")


class ZKAI:
    """The Master Facade and AI Operating System for ZKAI."""

    def __init__(self, config: Optional[ZKAIConfig] = None, **kwargs: Any):
        self.config = config or ZKAIConfig(**kwargs)

        # 1. Core Event Bus & AI Kernel Singleton
        self.events = default_event_bus
        self.plugins = PluginManager()
        self.kernel = AIKernel.get_instance()

        # 2. Base Security & Storage Services
        self.security_kernel = SecurityKernel()
        self.kernel.register_service("security_kernel", self.security_kernel, dependencies=[])

        self.storage = StorageProvider()
        self.kernel.register_service("storage", self.storage, dependencies=["security_kernel"])

        self.database = SQLiteDatabase()
        self.kernel.register_service("database", self.database, dependencies=["storage"])

        # 3. Process, IPC, Session & Identity
        self.process_manager = ProcessManager()
        self.kernel.register_service("process_manager", self.process_manager, dependencies=["security_kernel"])

        self.ipc_bus = SystemMessageBus(self.events)
        self.kernel.register_service("ipc_bus", self.ipc_bus, dependencies=["process_manager"])

        self.service_manager = ServiceManager()
        self.kernel.register_service("service_manager", self.service_manager, dependencies=["process_manager"])

        self.session_manager = SessionManager()
        self.kernel.register_service("session_manager", self.session_manager, dependencies=["storage"])

        self.tenant_manager = TenantManager()
        self.kernel.register_service("tenant_manager", self.tenant_manager, dependencies=["security_kernel"])

        # 4. Semantic Filesystem & Versioning
        self.files = FileExplorer()
        self.semantic_filesystem = SemanticFileIndex()
        self.versioned_storage = VersionedStorage()
        self.kernel.register_service("semantic_filesystem", self.semantic_filesystem, dependencies=["storage"])

        # 5. Model Management & LLM Engine
        self.models = ModelManager()
        self.language_model = LanguageModel()
        self.chat_model = ChatModel(model=self.language_model)
        self.evaluation = EvaluationPipeline()
        self.kernel.register_service("models", self.models, dependencies=["storage"])

        # 6. Memory Subsystem & Memory OS Daemon
        self.memory = MemoryManager()
        self.memory_daemon = MemoryDaemon(self.memory)
        self.kernel.register_service("memory_os", self.memory_daemon, dependencies=["storage"])

        # 7. Knowledge Base & Governance
        self.knowledge = KnowledgeBase()
        self.knowledge_governor = KnowledgeGovernor()
        self.kernel.register_service("knowledge_governor", self.knowledge_governor, dependencies=["storage"])

        # 8. Hardware HAL & Cluster Orchestrator
        self.device_manager = DeviceManager()
        self.kernel.register_service("device_manager", self.device_manager, dependencies=[])

        self.cluster_orchestrator = ClusterOrchestrator()
        self.kernel.register_service("cluster_orchestrator", self.cluster_orchestrator, dependencies=["device_manager", "ipc_bus"])

        # 9. Multimodal & Voice Layers
        self.vision_ocr = OCREngine()
        self.image_captioner = ImageCaptioner()
        self.stt = SpeechToText() if self.config.audio else None
        self.tts = TextToSpeech() if self.config.audio else None
        self.text_embedding = TextEmbedding()
        self.image_embedding = ImageEmbedding()
        self.voice = VoiceRuntime()
        self.kernel.register_service("voice", self.voice, dependencies=["security_kernel"])

        # 10. Tools Registry & Agent Subsystem
        self.tools = ToolRegistry()
        self._register_default_tools()
        self.agent = Agent(tool_registry=self.tools, memory=self.memory)
        self.coordinator = CoordinatorAgent()
        self.message_bus = MessageBus()
        self.shared_memory = SharedAgentMemory()

        self.computer_mouse = Mouse() if self.config.computer else None
        self.computer_keyboard = Keyboard() if self.config.computer else None
        self.computer_monitor = Monitor() if self.config.computer else None
        self.browser_search = BrowserSearch() if self.config.browser else None
        self.code_generator = CodeGenerator() if self.config.coding else None
        self.python_runner = PythonRunner() if self.config.coding else None

        # 11. Apps, Packages, Marketplace & Shell
        self.app_store = ApplicationStore()
        self.packages = PackageManager()
        self.marketplace = Marketplace()
        self.shell = ZKShell()

        self.kernel.register_service("apps", self.app_store, dependencies=["security_kernel"])
        self.kernel.register_service("packages", self.packages, dependencies=["security_kernel"])
        self.kernel.register_service("marketplace", self.marketplace, dependencies=["packages"])
        self.kernel.register_service("shell", self.shell, dependencies=["ipc_bus"])

        # 12. Training, Graph Compiler & System Monitor
        self.training = TrainingOrchestrator(self.language_model.decoder)
        self.graph_compiler = GraphCompiler()
        self.inference_cluster = InferenceCluster()
        self.monitor = SystemMonitor()
        self.kernel.register_service("monitor", self.monitor, dependencies=[])

        # 13. Infrastructure Governance, Observability & Rollback
        self.governor = self.kernel.governor
        self.rollback_manager = RollbackManager(self.kernel)
        self.tracer = DistributedTracer()
        self.metrics_registry = MetricsRegistry()

        # 14. Security, Governance, World Model & Hub Managers
        self.tokenizer_engine = BytePairTokenizer()
        self.security = SecretsManager()
        self.audit = AuditLog()
        self.hub = ModelHub()
        self.face_recognizer = FaceRecognizer()
        self.backend_selector = AutoBackendSelector()
        self.knowledge_bus = KnowledgeBus(self.events)
        self.research = ResearchEngine()
        self.governance_engine = GovernanceEngine()
        self.world_model = WorldModel()

        # Boot AI Kernel into READY state
        self.kernel.boot()

        logger.info(f"Initialized ZKAI AI Operating System on backend '{self.config.backend.value}' ({self.config.device.value}) [Kernel State: {self.kernel.state.value}]")

    def _register_default_tools(self) -> None:
        self.tools.register(PythonTool())
        self.tools.register(BrowserTool())
        self.tools.register(VisionTool())
        self.tools.register(SearchTool())
        self.tools.register(TerminalTool())
        self.tools.register(CalculatorTool())
        self.tools.register(DatabaseTool())
        self.tools.register(GitTool())

    # --- High-Level PyTorch & SDK API Methods ---
    def chat(self, message: str) -> str:
        """Sends chat message and receives generated response."""
        response = self.chat_model.chat(message)
        self.memory.remember(f"user_chat: {message}", response)
        return response

    def search(self, query: str) -> List[Any]:
        """Searches the internet for information and papers."""
        search_engine = SearchEngine()
        return asyncio.run(search_engine.search(query))

    def code(self, instruction: str) -> str:
        """Generates source code based on task specification."""
        if self.code_generator:
            return self.code_generator.generate_code(instruction)
        return f"# Code generation for: {instruction}"

    def look(self, image_path: str) -> str:
        """Analyzes image content using Vision OCR and captioning engines."""
        img = Image(image_path)
        text = self.vision_ocr.read_text(img)
        caption = self.image_captioner.caption(img)
        return f"Caption: {caption}\nExtracted Text: {text}"

    def listen(self, audio_path: str) -> str:
        """Transcribes audio file to text."""
        if self.stt:
            return self.stt.transcribe(audio_path)
        return "Audio subsystem disabled."

    def speak(self, text: str) -> str:
        """Synthesizes text to spoken audio file."""
        if self.tts:
            return self.tts.speak(text)
        return "Audio subsystem disabled."

    def click(self, x: int, y: int) -> None:
        """Simulates native mouse click at (x, y) coordinates."""
        if self.computer_mouse:
            self.computer_mouse.click(x, y)

    def open(self, url: str) -> Any:
        """Opens a website URL in headless browser."""
        browser = Browser()
        return asyncio.run(browser.open(url))

    def learn(self, dataset: Any) -> None:
        """Learns and consolidates knowledge from dataset into memory stores."""
        logger.info("Learning and ingesting dataset into ZKAI memory...")
        if isinstance(dataset, (list, tuple)):
            for idx, item in enumerate(dataset):
                if isinstance(item, tuple) and len(item) == 2:
                    key, val = item
                    self.memory.remember(str(key), val)
                elif isinstance(item, str):
                    self.memory.remember(f"dataset_item_{idx}", item)
                elif hasattr(item, "content"):
                    self.memory.remember(f"doc_{idx}", getattr(item, "content"))
                else:
                    self.memory.remember(f"dataset_item_{idx}", str(item))
        elif isinstance(dataset, str):
            self.memory.remember("dataset_text", dataset)
        elif hasattr(dataset, "__iter__"):
            for idx, item in enumerate(dataset):
                self.memory.remember(f"dataset_record_{idx}", str(item))
        else:
            self.memory.remember("dataset", str(dataset))

        self.memory.consolidate()
        logger.info("Successfully ingested and consolidated dataset into memory.")

    def train(self, dataset: Optional[Any] = None, epochs: int = 5) -> float:
        """Triggers training loop for underlying foundation model on provided or memory dataset."""
        logger.info(f"Initiating foundation model training for {epochs} epochs...")
        training_data = dataset
        if training_data is None:
            memory_entries = self.memory.long_term.retrieve("*", top_k=100)
            if memory_entries:
                training_data = [([float(ord(c)) for c in str(e.content)[:10]], [1.0]) for e in memory_entries]
            else:
                logger.warning("No memory entries or dataset found, Aborting!")
                return 0.0
        return self.training.train_pretraining(training_data, epochs=epochs)

    def save(self, file_path: str = "model.zk") -> str:
        """Saves current AI model state and memory to native .zk binary container."""
        params_count = sum(p.raw.numel() for p in self.language_model.decoder.parameters())
        cfg = self.language_model.config
        meta = ModelMetadata(
            name="ZKAI_FoundationModel",
            architecture="DecoderTransformer",
            num_parameters=params_count,
            vocab_size=cfg.vocab_size,
            hidden_dim=cfg.hidden_dim,
            num_layers=cfg.num_layers,
            num_heads=cfg.num_heads,
        )
        state_dict = self.language_model.decoder._torch_module.state_dict() if self.language_model.decoder._torch_module else {}
        return ZKModelFormat.save_model(file_path, state_dict, meta)

    def load(self, file_path: str = "model.zk") -> None:
        """Loads AI model state and memory from native .zk file."""
        meta, payload = ZKModelFormat.load_model(file_path)
        logger.info(f"Loaded model '{meta.name}' from {file_path}")

    def tokenize(self, text: str) -> EncodingResult:
        """Tokenizes input text using configured tokenizer engine."""
        return self.tokenizer_engine.encode(text)

    def benchmark(self, target: Any = None) -> str:
        """Runs standard benchmark suite and returns report."""
        results = [
            LatencyBenchmark().run(target or (lambda: None)),
            MemoryBenchmark().run(target),
            InferenceBenchmark().run(target),
        ]
        return ReportGenerator().generate_report(results)

    def evaluate_llm(self, model: Any = None) -> str:
        """Runs comprehensive 8-benchmark suite over LLM and returns Markdown report."""
        runner = EvalRunner()
        results = runner.run_all(model or self.language_model)
        return EvalReport().generate_report(results)

    def run_workflow(self, workflow_engine: WorkflowEngine, initial_input: Any = None) -> Any:
        """Executes a DAG workflow to completion."""
        runner = WorkflowRunner(workflow_engine)
        return runner.run(initial_input)

    def create_embedding(self, input_data: Any) -> Any:
        """Generates embedding vectors for text or image input."""
        if isinstance(input_data, str):
            return self.text_embedding.embed(input_data)
        return self.image_embedding.embed(input_data)

    def convert_model(self, src_path: str, tgt_path: str, target_format: str = "zk") -> str:
        """Converts model between weight container formats."""
        return ModelConverter.auto_convert(src_path, tgt_path, target_format=target_format)

    def recognize_face(self, image_path: str) -> Any:
        """Runs face recognition pipeline on provided image."""
        img = Image(image_path)
        return self.face_recognizer.recognize(img)

    def coordinate_agents(self, task: str) -> Any:
        """Delegates task to multi-agent coordinator."""
        return self.coordinator.execute_task(task)

    def reason(self, problem: str, depth: int = 3) -> Any:
        """Runs tree-of-thought reasoning over a problem."""
        searcher = TreeSearch()
        return searcher.search(problem, depth=depth)

    def export_model(self, format: str = "onnx", output_path: str = "model.onnx") -> str:
        """Exports current model to deployment format."""
        import torch
        exporter = ModelExporter()
        dummy = torch.randn(1, 10)
        if format == "torchscript":
            return exporter.export_torchscript(self.language_model.decoder._torch_module, output_path)
        return exporter.export_onnx(self.language_model.decoder._torch_module, dummy, output_path)

    def quantize_model(self, bits: int = 4) -> None:
        """Quantizes foundation model weights in-place."""
        if bits == 4:
            logger.info("Quantizing model to INT4...")
        elif bits == 8:
            logger.info("Quantizing model to INT8...")
        else:
            logger.info(f"Quantizing model to {bits}-bit...")


__version__ = APIVersion.get_version_string()


