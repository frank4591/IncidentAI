from domain.models import (
    Incident,
    Hypothesis,
    IncidentDecision,
    InvestigationAssessment,
)


class DecisionEngine:

    def make_decision(
        self,
        incident: Incident,
        hypotheses: list[Hypothesis],
        assessment: InvestigationAssessment,
    ) -> IncidentDecision:

        if (
            not assessment.sufficient_evidence
            or not hypotheses
        ):
            raise ValueError(
                "Cannot make incident decision "
                "with insufficient evidence."
            )

        selected = max(
            hypotheses,
            key=lambda h: h.confidence,
        )

        mapping = {
            "H-DB": (
                "DATABASE_CONNECTIVITY",
                "restart_server",
            ),
            "H-DEPLOY": (
                "DEPLOYMENT_REGRESSION",
                "rollback_deployment",
            ),
            "H-INFRA": (
                "INFRASTRUCTURE_FAILURE",
                "restart_server",
            ),
        }

        incident_type, action = mapping.get(
            selected.hypothesis_id,
            ("UNKNOWN", "no_action"),
        )

        return IncidentDecision(
            incident_type=incident_type,
            accepted_hypotheses=[
                selected.hypothesis_id
            ],
            rejected_hypotheses=[
                h.hypothesis_id
                for h in hypotheses
                if h.hypothesis_id
                != selected.hypothesis_id
            ],
            reason=selected.statement,
            confidence=selected.confidence,
            proposed_action=action,
        )