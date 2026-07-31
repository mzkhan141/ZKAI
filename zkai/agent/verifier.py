"""AgentVerifier and Evaluator."""

from zkai.agent.goal import Goal


class AgentVerifier:
    """Verifies whether a Goal has been satisfied."""

    def verify_goal_completion(self, goal: Goal) -> bool:
        return all(sub.completed for sub in goal.subtasks) if goal.subtasks else True
