from typing import Protocol


from domain.models import (
    Evidence,
    Incident,
    Hypothesis,
    InvestigationAssessment,
    ExecutionPlan
)

class Planner(Protocol):

    async def create_plan(
        self,
        incident: Incident,
        evidence: list[Evidence],
        hypotheses: list[Hypothesis],
        assessment: InvestigationAssessment | None,
        iteration: int,
    ) -> ExecutionPlan:
        ...