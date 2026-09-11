from domain.models import (
    Evidence,
    Hypothesis,
    Incident,
    IncidentDecision,
    InvestigationAssessment,
)


class DecisionEngine:

    async def make_decision(
        self,
        incident: Incident,
        evidence: list[Evidence],
        hypotheses: list[Hypothesis],
        assessment: InvestigationAssessment,
    ) -> IncidentDecision:

        if not assessment.sufficient_evidence:
            raise ValueError(
                "Decision cannot be made because "
                "investigation evidence is insufficient."
            )

        if not hypotheses:
            raise ValueError(
                "Cannot make decision without hypotheses."
            )

        ranked = sorted(
            hypotheses,
            key=lambda h: h.confidence,
            reverse=True,
        )

        selected = ranked[0]

        rejected = [
            h.hypothesis_id
            for h in ranked[1:]
        ]

        action = self._determine_action(
            incident=incident,
            hypothesis=selected,
        )

        return IncidentDecision(
            incident_type=self._incident_type(
                selected
            ),
            accepted_hypotheses=[
                selected.hypothesis_id
            ],
            rejected_hypotheses=rejected,
            reason=(
                f"Selected hypothesis "
                f"{selected.hypothesis_id}: "
                f"{selected.statement}"
            ),
            confidence=selected.confidence,
            proposed_action=action,
        )

    def _incident_type(
        self,
        hypothesis: Hypothesis,
    ) -> str:

        statement = hypothesis.statement.lower()

        if "database" in statement:
            return "DATABASE_CONNECTIVITY"

        if "deployment" in statement:
            return "DEPLOYMENT_REGRESSION"

        if "infrastructure" in statement:
            return "INFRASTRUCTURE_FAILURE"

        return "UNKNOWN"

    def _determine_action(
        self,
        incident: Incident,
        hypothesis: Hypothesis,
    ) -> str:

        statement = hypothesis.statement.lower()

        if "database" in statement:
            return "restart_server"

        if "deployment" in statement:
            return "rollback_deployment"

        if "infrastructure" in statement:
            return "restart_server"

        return "NO_ACTION"