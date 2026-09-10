class RetryPolicy:

    def __init__(
        self,
        max_attempts: int = 2,
    ):
        self.max_attempts = max_attempts

    def should_retry(
        self,
        attempt: int,
    ) -> bool:

        return attempt < self.max_attempts