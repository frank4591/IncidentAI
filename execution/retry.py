from dataclasses import dataclass


@dataclass
class RetryDecision:
    should_retry: bool
    next_attempt: int
    reason: str


class RetryPolicy:

    def __init__(
        self,
        max_attempts: int = 2,
    ):
        self.max_attempts = max_attempts

    def evaluate(
        self,
        current_attempt: int,
        execution_status: str,
    ) -> RetryDecision:

        if execution_status == "SUCCESS":

            return RetryDecision(
                should_retry=False,
                next_attempt=current_attempt,
                reason="Execution succeeded.",
            )

        if current_attempt >= self.max_attempts:

            return RetryDecision(
                should_retry=False,
                next_attempt=current_attempt,
                reason=(
                    "Maximum retry attempts exhausted."
                ),
            )

        return RetryDecision(
            should_retry=True,
            next_attempt=current_attempt + 1,
            reason=(
                f"Retrying action. "
                f"Attempt {current_attempt + 1} "
                f"of {self.max_attempts}."
            ),
        )