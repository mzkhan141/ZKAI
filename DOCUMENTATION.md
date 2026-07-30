# ZKAI — Complete End-User Documentation & Master Reference Guide

Welcome to the official, complete end-user documentation for the **ZKAI AI Operating System & Framework**.

---

## Table of Contents

1. [Introduction & Core Philosophy](#1-introduction--core-philosophy)
2. [Installation & Setup](#2-installation--setup)
3. [The Unified Gateway (`from zkai import *`)](#3-the-unified-gateway)
4. [Subsystem Architecture & Microkernel Map](#4-subsystem-architecture--microkernel-map)
5. [Neural & Transformer Engine](#5-neural--transformer-engine)
6. [Memory, Knowledge & Vector Storage](#6-memory-knowledge--vector-storage)
7. [Agents, Workflows & Reasoning Engines](#7-agents-workflows--reasoning-engines)
8. [Multimodal Vision, Audio & Video Processing](#8-multimodal-vision-audio--video-processing)
9. [Computer Automation & Desktop Tools](#9-computer-automation--desktop-tools)
10. [Security, Capability OS & Sandboxing](#10-security-capability-os--sandboxing)
11. [Distributed Training, Quantization & PEFT](#11-distributed-training-quantization--peft)
12. [Robotics, Devices & Hardware IO](#12-robotics-devices--hardware-io)
13. [Subsystem Class Reference](#13-subsystem-class-reference)
14. [Troubleshooting & Graceful Degradation](#14-troubleshooting--graceful-degradation)

---

## 1. Introduction & Core Philosophy

ZKAI is a **native AI Operating System** written in Python. It does not rely on heavy third-party framework wrappers. Instead, it provides a single unified environment combining:
- High-level multi-agent orchestration
- Microkernel fault recovery and intelligent scheduling
- Low-level neural network operations and transformer inference
- Multimodal I/O (Vision, Speech, Audio, Video, Desktop Automation)
- Enterprise security, sandboxing, and capability-based RBAC

### Key Principles

1. **Single Entry Point**: All classes, engines, and tools are re-exported under `from zkai import *`.
2. **Zero Hard Dependencies**: All heavy or specialized hardware drivers (like `faiss`, `opencv-python`, `easyocr`, `playwright`) gracefully degrade to pure Python fallbacks if not installed.
3. **Microkernel Architecture**: Decoupled kernel services communicate via a thread-safe `KnowledgeBus`.
4. **Self-Healing Resilience**: Intercepts unexpected faults during execution and repairs task state automatically.

---

## 2. Installation & Setup

### Basic Installation

```bash
git clone https://github.com/zk-ai/zkai.git
cd zkai
pip install -e .
```

### Full Installation (Multimodal & Performance Extras)

```bash
# Install with all optional drivers (CV, Audio, Vector DB, Server, Automation)
pip install -e .[all]
```

### Environmental Requirements
- **Python**: `3.10` or higher (`3.12+` recommended).
- **Operating Systems**: Windows, macOS, Linux.
- **Hardware**: CPU, NVIDIA CUDA, AMD ROCm, Apple Metal, or Vulkan.

---

## 3. The Unified Gateway

The fastest way to use ZKAI is through the high-level `ZKAI` facade object.

```python
from zkai import *

# Initialize the AI OS
ai = ZKAI()

# 1. Direct Conversational Inference
reply = ai.chat("Explain the difference between synchronous and asynchronous IO.")

# 2. Tool Execution
tool_result = ai.execute_tool("calculator", expression="2 ** 10")
print("1024 =", tool_result.result)

# 3. Spawn Isolated Virtual AI (Multi-Tenancy)
vm = ai.spawn_virtual_ai("vm-analyst", profile="Data Scientist")
analysis = ai.chat_virtual("vm-analyst", "How do I calculate standard deviation?")

# 4. Fault-Tolerant Execution
def risky_operation():
    return "Operations completed successfully."

success, output = ai.execute_with_healing(risky_operation)
```

---

## 4. Subsystem Architecture & Microkernel Map

ZKAI is structured into **15 Core Kernel Subsystems** orchestrated by the `AIKernel`:

```
                           +------------------------+
                           |      ZKAI Facade       |
                           +-----------+------------+
                                       |
                           +-----------+------------+
                           |        AIKernel        |
                           +-----------+------------+
                                       |
    +-------------------+--------------+--------------+-------------------+
    |                   |                             |                   |
+---+---------------+ +-+------------------+       +--+----------------+ +---+---------------+
|   CapabilityOS    | |   MicroKernel      |       |   KnowledgeBus    | | AIHypervisor      |
| (Access & Security)| | (Thread Primitive) |       | (IPC & Messaging) | | (Virtual AIs)     |
+-------------------+ +--------------------+       +-------------------+ +-------------------+
```

### Kernel Engines Summary

1. **`MicroKernel`**: Manages low-level task switching, thread-safe memory allocations, and state machines.
2. **`CapabilityOS`**: Enforces rule-based security permissions for disk, network, and system execution.
3. **`AIHypervisor`**: Instantiates and isolates virtual AI instances (`VirtualAI`).
4. **`SelfHealingManager`**: Intercepts unhandled runtime exceptions, performs state rollbacks, and retries tasks.
5. **`EvolutionEngine`**: Tracks execution history and refines agent prompts over time.
6. **`KnowledgeBus`**: Pub/sub messaging system bridging events across agents and subsystems.
7. **`CognitiveRuntime`**: Manages short-term working memory and multi-step reasoning loops.
8. **`SimulationEngine`**: Dry-runs tool calls in isolated environments before executing live.
9. **`AutonomousResearch`**: Automatically queries internet search engines and compiles literature summaries.
10. **`GovernanceEngine`**: Monitors resource quotas, ethical constraints, and compliance checks.
11. **`DigitalTwin`**: Maintains state models predicting user preferences and process behavior.
12. **`AutonomousTesting`**: Runs background chaos-injection tests to ensure system resilience.
13. **`SemanticScheduler`**: Schedules workload queues based on urgency, GPU memory, and priority.
14. **`WorldModel`**: Graph database tracking entities, properties, and relationships.
15. **`KernelIntelligence`**: Master coordinator binding all kernel engines together.

---

## 5. Neural & Transformer Engine

ZKAI contains a full native neural network library and transformer architecture.

### Building Custom Neural Networks

```python
from zkai import *

# Define a Multi-Layer Perceptron (MLP)
model = Sequential(
    Linear(784, 256),
    ReLU(),
    Dropout(0.2),
    Linear(256, 10),
    Softmax()
)

optimizer = AdamW(model.parameters(), lr=1e-3)
criterion = CrossEntropyLoss()

# Synthetic Forward & Backward Pass
inputs = Tensor.randn(32, 784)
targets = Tensor.zeros(32, dtype=DType.INT64)

outputs = model(inputs)
loss = criterion(outputs, targets)
optimizer.step()

print("Loss:", loss.item())
```

### Transformer Attention & Token Streaming

```python
from zkai import *

# Initialize Rotary Position Embeddings and Flash Attention
rotary = RotaryEmbedding(dim=64)
attn = MultiHeadAttention(embed_dim=512, num_heads=8)

# Token Streamer for real-time inference
streamer = TokenStreamer(timeout=5.0)
streamer.put("Hello ")
streamer.put("World!")
streamer.end()

for token in streamer:
    print(token, end="")
```

---

## 6. Memory, Knowledge & Vector Storage

ZKAI provides 14 distinct memory primitives managed by `MemoryManager`.

```python
from zkai import *

# 1. Dense Vector Memory
vector_mem = VectorMemory(dimension=384)
vector_mem.store_vector("fact-1", "Python is a dynamic programming language.", [0.1] * 384)

# 2. Episodic Memory
episodic_mem = EpisodicMemory()
episodic_mem.record_episode(task="Data Analysis", result="Passed with 99% accuracy")

# 3. Hierarchical Working Memory
working_mem = HierarchicalWorkingMemory()
working_mem.push_context("Session 102", {"user": "Alice"})
```

---

## 7. Agents, Workflows & Reasoning Engines

Build autonomous AI agents with tree-search reasoning and DAG workflow graph capabilities.

```python
from zkai import *

# 1. Create an Agent with Goals
agent = Agent(name="ResearcherAgent", role="Academic Analyst")
goal = Goal(description="Analyze recent quantum computing papers")
agent.add_goal(goal)

# 2. Plan and Execute
planner = AgentPlanner()
plan = planner.create_plan(agent, goal)
print("Generated Plan Steps:", [step.description for step in plan.steps])

# 3. Tree-of-Thought Reasoning
tot = TreeOfThought(max_depth=3)
solution = tot.solve(prompt="How do we optimize database queries for 10M rows?")
print("Reasoning Solution:", solution)
```

---

## 8. Multimodal Vision, Audio & Video Processing

Processing images, audio streams, and video files natively:

```python
from zkai import *

# 1. Optical Character Recognition (OCR)
ocr = OCREngine()
image = Image("sample_screenshot.png")
text = ocr.read_text(image)
print("Extracted Text:", text)

# 2. Speech-to-Text Transcription
stt = SpeechToText()
transcript = stt.transcribe("recorded_audio.wav")
print("Transcript:", transcript)

# 3. Video Frame Analysis
video = Video("input_clip.mp4")
print(f"Video Info: {video.duration_seconds}s, FPS: {video.fps}")
```

---

## 9. Computer Automation & Desktop Tools

Automate mouse movements, window operations, web browsing, and shell execution securely.

```python
from zkai import *

# 1. Web Search Tool
search_tool = SearchTool()
results = search_tool.execute(query="ZKAI framework documentation")
print("Search Results:", len(results.result))

# 2. Secure Calculator Tool
calc_tool = CalculatorTool()
result = calc_tool.execute(expression="(100 + 50) / 2")
print("Calc Result:", result.result)

# 3. Desktop Automation
mouse = Mouse()
mouse.move_to(100, 200)
```

---

## 10. Security, Capability OS & Sandboxing

All I/O operations are validated by `CapabilityOS` and `SandboxPolicy`.

```python
from zkai import *

cap_os = CapabilityOS()

# Grant specific filesystem permission
cap_os.grant(CapabilityRule(
    capability_name="filesystem_read",
    resource_pattern="/data/public/*",
    allowed=True
))

# Verify permission before file access
is_allowed = cap_os.check_permission("filesystem_read", "/data/public/report.csv")
print("Permission Granted:", is_allowed) # True
```

---

## 11. Distributed Training, Quantization & PEFT

Fine-tune models efficiently with INT4, NF4, FP8 quantization, and LoRA adapters.

```python
from zkai import *

# 1. Apply LoRA Adapter
lora_config = LoRAConfig(r=8, lora_alpha=16, target_modules=["query", "value"])
adapter = LoRAAdapter(config=lora_config)

# 2. Quantize Weights to INT4
quantizer = INT4Quantizer()
packed_weights = quantizer.quantize(Tensor.randn(1024, 1024))
print("Quantized Weight Shape:", packed_weights.shape)
```

---

## 12. Robotics, Devices & Hardware IO

Control GPIO pins, serial devices, and ROS bridges directly:

```python
from zkai import *

# Initialize Robot Device
robot = Robot(name="Rover-01")
gpio = GPIO()
gpio.setup_pin(pin=18, mode="OUT")
gpio.write_pin(pin=18, value=1)
print("Robot Status:", robot.get_status())
```

---

## 13. Subsystem Class Reference

Here is a quick lookup table of key classes available via `from zkai import *`:

| Module | Core Classes |
| :--- | :--- |
| **`zkai.core`** | `ZKAIConfig`, `Logger`, `EventBus`, `TaskExecutor`, `PluginRegistry`, `DiskCache` |
| **`zkai.neural`** | `Tensor`, `Module`, `Linear`, `Conv2D`, `AdamW`, `CrossEntropyLoss`, `Trainer` |
| **`zkai.transformer`**| `MultiHeadAttention`, `FlashAttention`, `KVCache`, `TokenStreamer`, `InferenceEngine` |
| **`zkai.memory`** | `MemoryManager`, `VectorMemory`, `EpisodicMemory`, `WorkingMemory`, `GraphMemory` |
| **`zkai.agent`** | `Agent`, `Goal`, `AgentPlanner`, `AgentExecutor`, `AutonomousExecutor` |
| **`zkai.tools`** | `Tool`, `ToolRegistry`, `CalculatorTool`, `SearchTool`, `BrowserTool`, `VisionTool` |
| **`zkai.kernel`** | `AIKernel`, `MicroKernel`, `AIHypervisor`, `SelfHealingManager`, `KnowledgeBus` |
| **`zkai.security`** | `CapabilityOS`, `GovernanceEngine`, `PermissionEngine`, `AuditLog`, `SandboxPolicy` |

---

## 14. Troubleshooting & Graceful Degradation

If specialized binary packages (`faiss-cpu`, `opencv-python`, `easyocr`, `playwright`) are missing from your environment, ZKAI automatically degrades to native Python implementations:

- **Missing FAISS**: Reverts to `NumPyVectorStore` (Cosine Similarity).
- **Missing OpenCV**: Reverts to native image stubs.
- **Missing EasyOCR**: Reverts to native pattern matching fallback.
- **Missing Playwright**: Reverts to `aiohttp` HTML scrapers.

All core features, neural networks, agents, and security capabilities run out of the box with zero required C-extension dependencies!
