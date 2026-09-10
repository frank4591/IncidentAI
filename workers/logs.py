from datetime import datetime, timezone

from domain.models import (
    Evidence,
    Incident,
    WorkerResult,
    WorkerTask,
)


class LogsWorker:

    @property
    def capability(self) -> str:
        return "logs_analysis"

    async def execute(
        self,
        task: WorkerTask,
        incident: Incident,
    ) -> WorkerResult:

        evidence = [
            Evidence(
                evidence_id=f"{task.task_id}-e1",
                source="application_logs",
                category="DATABASE",
                observation=(
                    "Repeated database connection timeout "
                    "and pool exhaustion detected."
                ),
                confidence=0.85,
                timestamp=datetime.now(timezone.utc),
                metadata={
                    "service": incident.service
                },
            )
        ]

        return WorkerResult(
            task_id=task.task_id,
            worker_name="LogsWorker",
            status="SUCCESS",
            evidence=evidence,
            duration_ms=50,
        )