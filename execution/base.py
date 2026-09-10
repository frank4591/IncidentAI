from typing import Protocol

from domain.models import (
    ExecutionResult,
    Incident,
)


class Executor(Protocol):

    async def execute(
        self,
        action: str,
        incident: Incident,
        attempt: int,
    ) -> ExecutionResult:
        ...