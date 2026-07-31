"""ContinuousBatcher, DynamicBatchScheduler, and SequenceScheduler for continuous iteration-level batching."""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("transformer.continuous_batcher")


@dataclass
class SequenceRequest:
    """Represents a single generation request in continuous batching queue."""

    request_id: str
    prompt_tokens: List[int]
    max_new_tokens: int = 128
    arrival_time: float = field(default_factory=time.time)
    generated_tokens: List[int] = field(default_factory=list)
    is_finished: bool = False


class SequenceScheduler:
    """Priority request queue for sequence generation scheduling."""

    def __init__(self, max_batch_size: int = 32):
        self.max_batch_size = max_batch_size
        self.pending_requests: List[SequenceRequest] = []

    def add_request(self, req: SequenceRequest) -> None:
        self.pending_requests.append(req)

    def get_next_batch(self, active_count: int) -> List[SequenceRequest]:
        available_slots = max(0, self.max_batch_size - active_count)
        next_batch = self.pending_requests[:available_slots]
        self.pending_requests = self.pending_requests[available_slots:]
        return next_batch


class DynamicBatchScheduler:
    """Dynamically adjusts batch size based on active context lengths and system memory constraints."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def select_active_sequences(self, requests: List[SequenceRequest]) -> List[SequenceRequest]:
        active = []
        total_tokens = 0
        for req in requests:
            seq_len = len(req.prompt_tokens) + len(req.generated_tokens)
            if total_tokens + seq_len <= self.max_tokens:
                active.append(req)
                total_tokens += seq_len
            else:
                break
        return active or requests[:1]


class ContinuousBatcher:
    """vLLM-style continuous batching engine scheduling iteration-level prefill & decode steps."""

    def __init__(self, max_batch_size: int = 32, max_tokens: int = 4096):
        self.scheduler = SequenceScheduler(max_batch_size)
        self.dynamic_scheduler = DynamicBatchScheduler(max_tokens)
        self.running_requests: List[SequenceRequest] = []

    def add_request(self, request_id: str, prompt_tokens: List[int], max_new_tokens: int = 128) -> SequenceRequest:
        req = SequenceRequest(request_id=request_id, prompt_tokens=prompt_tokens, max_new_tokens=max_new_tokens)
        self.scheduler.add_request(req)
        return req

    def step(self) -> List[SequenceRequest]:
        """Executes one continuous decoding iteration over active batch."""
        new_reqs = self.scheduler.get_next_batch(len(self.running_requests))
        self.running_requests.extend(new_reqs)

        active = self.dynamic_scheduler.select_active_sequences(self.running_requests)

        for req in active:
            # Simulate decoding single token
            next_token = 42
            req.generated_tokens.append(next_token)
            if len(req.generated_tokens) >= req.max_new_tokens:
                req.is_finished = True

        self.running_requests = [r for r in self.running_requests if not r.is_finished]
        return active
