from domain.models import (
    ExecutionResult,
    Incident,
)


class ServerRestartExecutor:

    async def execute(
        self,
        action: str,
        incident: Incident,
        attempt: int,
    ) -> ExecutionResult:

        print(
            f"[MOCK] Restarting server "
            f"for {incident.service}; "
            f"attempt={attempt}"
        )

        return ExecutionResult(
            action=action,
            status="SUCCESS",
            attempt=attempt,
            output={
                "service": incident.service,
                "mock": True,
            },
        )