from domain.models import (
    ExecutionResult,
    Incident,
    VerificationResult,
)


class ServiceVerifier:

    async def verify(
        self,
        incident: Incident,
        execution: ExecutionResult,
    ) -> VerificationResult:

        healthy = (
            execution.status == "SUCCESS"
        )

        return VerificationResult(
            verified=healthy,
            service_healthy=healthy,
            alert_cleared=healthy,
            observations=[
                "Mock service health check completed."
            ],
            reason=(
                "Service healthy and alert cleared."
                if healthy
                else "Service remains unhealthy."
            ),
        )