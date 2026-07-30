# ZKAI — Production-Grade Native AI Operating System

<p align="center">
  <strong>The Unified, Self-Healing, Multi-Tenant AI Operating System for Python.</strong><br>
  <em>Microkernel · Neural Engine · Hypervisor · Knowledge Bus · Self-Healing · Cognitive Runtime · Capability Security — All bound under one simple import.</em>
</p>

<p align="center">
  <a href="#what-is-zkai-non-technical-overview">Non-Technical Overview</a> •
  <a href="#quick-start-guide">Quick Start</a> •
  <a href="#architecture--subsystems">Architecture</a> •
  <a href="#step-by-step-tutorials">Tutorials</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#type-documentation">Types & Config</a>
</p>

---

```python
from zkai import *

# Initialize the complete AI Operating System
ai = ZKAI()

# Run chat, reasoning, tool execution, and memory retrieval automatically
response = ai.chat("What is the speed of light in vacuum?")
print(response)
```

---

## What is ZKAI? (Non-Technical Overview)

Think of how **Windows** or **macOS** manages your computer's hardware—allocating memory, running applications, preventing crashes, and keeping your files safe. 

**ZKAI is an Operating System built specifically for Artificial Intelligence.**

Instead of managing physical hardware like disk drives and graphics cards, ZKAI manages **AI brains, knowledge, memory, tools, and reasoning processes**. It allows software developers to run intelligent AI agents safely, smoothly, and without worrying about underlying complex machine learning plumbing.

### Why ZKAI?

- 🧠 **One Simple Gateway**: You don't need to learn 20 different libraries. `from zkai import *` gives you everything.
- 🛡️ **Built-in Security**: Prevents AI agents from running harmful commands or stealing data without permission.
- 🩹 **Self-Healing**: If an AI task fails or crashes, ZKAI automatically diagnoses the error, repairs state, and retries seamlessly.
- 🔌 **Works Anywhere**: ZKAI includes native Python fallbacks for all AI models, so it runs even on basic laptops without expensive GPUs.

---

## Quick Start Guide

### Installation

```bash
# Clone the repository
git clone https://github.com/mzkhan141/ZKAI.git
cd zkai

# Install core package
pip install -e .

# Optional: Install all vision, audio, and server extras
pip install -e .[all]
```

### Your First AI Script

Save the following code as `first_ai.py` and run it:

```python
from zkai import *

# Boot up ZKAI Kernel
ai = ZKAI()

# Ask a question
reply = ai.chat("Explain quantum computing in simple terms.")
print("AI Reply:", reply)

# Execute a safe mathematical calculation
result = ai.execute_tool("calculator", expression="42 * 1337")
print("Calculation Result:", result.result)
```

---

## Architecture & Subsystems

ZKAI is structured around an **Intelligent Microkernel Topology**. High-level reasoning engines, security governance, and digital twin simulators run as decoupled services communicating over a semantic `KnowledgeBus`.

```
                    +--------------------------------+
                    |        ZKAI Facade API         |
                    +---------------+----------------+
                                    |
                    +---------------+----------------+
                    |           AIKernel             |
                    +---------------+----------------+
                                    |
         +--------------------------+--------------------------+
         |                          |                          |
+--------+-------+          +-------+--------+        +--------+-------+
|  MicroKernel   |          |  KnowledgeBus  |        | CapabilityOS   |
| (State & IPC)  |          | (Events & Msg) |        | (RBAC & Rules) |
+--------+-------+          +-------+--------+        +--------+-------+
         |                          |                          |
+--------+-------+          +-------+--------+        +--------+-------+
|  AIHypervisor  |          |SelfHealing Engine       |Governance Engine|
|(Virtual AIs)   |          | (Fault Recovery)       | (Ethics/Policy)|
+----------------+          +----------------+        +----------------+
```

### 15 Core Intelligent Kernel Subsystems

| Subsystem | Class Name | Purpose |
| :--- | :--- | :--- |
| **MicroKernel** | `MicroKernel` | Low-overhead core handling thread IPC and primitive state. |
| **Capability OS** | `CapabilityOS` | Enforces permissions and sandboxing before any I/O execution. |
| **Hypervisor** | `AIHypervisor` | Manages isolated multi-tenant `VirtualAI` instances. |
| **Self-Healing** | `SelfHealingManager` | Automatically intercepts errors, repairs corrupted state, and retries tasks. |
| **Evolution Engine**| `EvolutionEngine` | Self-optimizes prompt strategies and task routing over time. |
| **Knowledge Bus** | `KnowledgeBus` | High-throughput semantic message bus bridging events across agents. |
| **Cognitive Runtime**| `CognitiveRuntime` | Manages step-by-step reasoning streams and context memory. |
| **Simulation Engine**| `SimulationEngine` | Dry-runs workflows in virtual environments to score risk before execution. |
| **Research Engine**| `AutonomousResearch` | Automatically searches, aggregates, and summarizes external literature. |
| **Governance Engine**| `GovernanceEngine` | Evaluates safety policies, ethical alignment, and resource quotas. |
| **Digital Twin** | `DigitalTwin` | Builds predictive state models of external processes and user habits. |
| **Chaos Testing** | `AutonomousTesting` | Injects synthetic faults to continuously stress-test resilience. |
| **Semantic Scheduler**| `SemanticScheduler` | Schedules tasks based on priority goals, GPU load, and urgency. |
| **World Model** | `WorldModel` | Maintains structured relational knowledge graphs of entities and facts. |
| **Kernel Intelligence**| `KernelIntelligence` | Central supervisor orchestrating all 14 intelligent kernel engines. |

---

## Step-by-Step Tutorials

### Tutorial 1: Building an Agent with Tools

Learn how to equip an AI agent with Web Search, Vision, and Calculator capabilities:

```python
from zkai import *

# 1. Initialize ZKAI
ai = ZKAI()

# 2. Register tools
ai.register_tool(CalculatorTool())
ai.register_tool(SearchTool())

# 3. Create an agent context
context = ToolContext(user_query="Calculate 15% tip on $85.00")

# 4. Select best tool automatically
best_tool = ai.select_tool(context)
print(f"Selected Tool: {best_tool.metadata.name}")

# 5. Execute tool safely
res = ai.execute_tool(best_tool.metadata.name, expression="85.00 * 0.15")
print(f"Result: ${res.result:.2f}")
```

### Tutorial 2: Isolated Virtual AIs (Multi-Tenancy)

Run multiple isolated AI instances side-by-side using the `AIHypervisor`:

```python
from zkai import *

ai = ZKAI()

# Spawn Virtual AI 1 for Finance
finance_vm = ai.spawn_virtual_ai(vm_id="vm-finance", profile="Financial Advisor")

# Spawn Virtual AI 2 for Coding
coding_vm = ai.spawn_virtual_ai(vm_id="vm-coding", profile="Senior Python Dev")

# Execute isolated workloads
res1 = ai.chat_virtual("vm-finance", "How do I calculate CAGR?")
res2 = ai.chat_virtual("vm-coding", "Write a Python quicksort implementation.")

print("Finance VM:", res1)
print("Coding VM:", res2)
```

### Tutorial 3: Self-Healing Fault Recovery

Demonstrating ZKAI's ability to intercept failures and self-heal automatically:

```python
from zkai import *

ai = ZKAI()

# Define a function that temporarily fails
attempt_count = 0
def fragile_task():
    global attempt_count
    attempt_count += 1
    if attempt_count < 2:
        raise ConnectionError("Temporary network glitch")
    return "Task Succeeded!"

# Execute via SelfHealing Engine
success, result = ai.execute_with_healing(fragile_task)
print(f"Healed Execution Status: {success}, Result: {result}")
```

---

## API Reference

All primary interfaces are accessible directly through `from zkai import *`.

### Facade Entry Point: `ZKAI`

```python
class ZKAI:
    def __init__(self): ...
    def chat(self, prompt: str) -> str: ...
    def register_tool(self, tool: Tool) -> None: ...
    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult: ...
    def spawn_virtual_ai(self, vm_id: str, profile: str = "Standard") -> VirtualAI: ...
    def chat_virtual(self, vm_id: str, prompt: str) -> str: ...
    def execute_with_healing(self, fn: Callable) -> Tuple[bool, Any]: ...
```

### Subsystem Reference

#### `CapabilityOS`
Enforces fine-grained permission rules before allowing operations.
- `grant(rule: CapabilityRule) -> None`: Adds an allowed capability rule.
- `revoke(capability_name: str) -> None`: Revokes a permission.
- `check_permission(capability_name: str, resource: str) -> bool`: Validates access.

#### `KnowledgeBus`
Thread-safe event pub/sub bus for inter-agent communication.
- `publish(topic: str, data: Any) -> None`: Broadcasts a payload onto a topic.
- `subscribe(topic: str, handler: Callable) -> None`: Subscribes a callback to a topic.

---

## Master Documentation

For complete, in-depth end-user guides, API references, neural network building tutorials, and hardware I/O documentation, please see the exhaustive master reference guide:

📖 **[Read the Complete ZKAI Master Documentation](DOCUMENTATION.md)**

---

## License

ZKAI is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.
