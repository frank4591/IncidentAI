import asyncio
from time import perf_counter
from typing import Protocol


from domain.models import (
    Incident,
    ExecutionPlan,
    WorkerResult,
    WorkerTask,
)

class Scheduler(Protocol):

    async def execute(
        self,
        plan: ExecutionPlan,
        incident: Incident,
    ) -> list[WorkerResult]:
        ...


class LocalScheduler:

    def __init__(
        self,
        registry,
        timeout_seconds: float = 10,
    ):
        self.registry = registry
        self.timeout_seconds = timeout_seconds

    async def _run_one(
        self,
        task: WorkerTask,
        incident: Incident,
    ) -> WorkerResult:

        start = perf_counter()

        try:

            worker = self.registry.resolve(
                task.capability
            )

            result = await asyncio.wait_for(
                worker.execute(task, incident),
                timeout=self.timeout_seconds,
            )

            if result.duration_ms is None:
                result.duration_ms = int(
                    (perf_counter() - start) * 1000
                )

            return result

        except asyncio.TimeoutError:

            return WorkerResult(
                task_id=task.task_id,
                worker_name=task.capability,
                status="TIMEOUT",
                evidence=[],
                error="worker timeout",
                duration_ms=int(
                    (perf_counter() - start) * 1000
                ),
            )

        except Exception as exc:

            return WorkerResult(
                task_id=task.task_id,
                worker_name=task.capability,
                status="FAILED",
                evidence=[],
                error=str(exc),
                duration_ms=int(
                    (perf_counter() - start) * 1000
                ),
            )

    async def execute(
        self,
        tasks: list[WorkerTask],
        incident: Incident,
    ) -> list[WorkerResult]:

        return await asyncio.gather(
            *(
                self._run_one(task, incident)
                for task in tasks
            )
        )