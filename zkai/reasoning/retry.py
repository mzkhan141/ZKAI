"""RetryPlanner for adaptive retry strategies."""

from zkai.evaluation.retry import RetryManager


class RetryPlanner:
    """Manages adaptive retry attempts with strategy escalation."""

    def __init__(self, max_retries: int = 3):
        self.manager = RetryManager(max_retries=max_retries)

    def should_retry(self, attempt: int) -> bool:
        return self.manager.can_retry(attempt)
