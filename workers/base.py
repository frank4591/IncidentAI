from typing import Protocol

from domain.models import (
    Incident,
    WorkerResult,
    WorkerTask,
)


class Worker(Protocol):

    @property
    def capability(self) -> str:
        ...

    async def execute(
        self,
        task: WorkerTask,
        incident: Incident,
    ) -> WorkerResult:
        ...


class WorkerRegistry(Protocol):

    def resolve(self, capability: str) -> Worker:
        ...