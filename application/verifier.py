from typing import Protocol


from domain.models import (
    Incident,
    ActionRequest,
    ExecutionResult,
    VerificationResult,
)
class Verifier(Protocol):

    async def verify(
        self,
        incident: Incident,
        action: ActionRequest,
        execution: ExecutionResult,
    ) -> VerificationResult:
        ...