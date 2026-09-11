from domain.models import (
    Incident,
    IncidentDecision,
    PolicyEvaluation,
    RiskAssessment,
)

# class PolicyEngine(Protocol):

#     async def evaluate(
#         self,
#         incident: Incident,
#         decision: IncidentDecision,
#         action: ActionRequest,
#         risk: RiskAssessment,
#         policies: list[PolicyRule],
#     ) -> PolicyEvaluation:
#         ...

class PolicyEngine:

    def evaluate(
        self,
        incident: Incident,
        decision: IncidentDecision,
        action: str,
        risk: RiskAssessment,
        policies: list[dict],
    ) -> PolicyEvaluation:

        matches = []
        outcomes = []

        context = {
            "environment": incident.environment,
            "severity": incident.severity,
            "action": action,
            "risk_level": risk.risk_level,
        }

        for policy in policies:

            conditions = policy.get(
                "conditions",
                {},
            )

            if all(
                context.get(key) == value
                for key, value
                in conditions.items()
            ):

                matches.append(
                    policy["policy_id"]
                )

                outcomes.append(
                    policy["outcome"]
                )

        # Explicit DENY always wins.
        if "DENY" in outcomes:

            return PolicyEvaluation(
                permitted=False,
                approval_required=False,
                matched_policy_ids=matches,
                reason=(
                    "Explicit DENY policy matched."
                ),
                confidence=1.0,
            )

        # HITL takes precedence over ALLOW.
        if "HITL" in outcomes:

            return PolicyEvaluation(
                permitted=True,
                approval_required=True,
                matched_policy_ids=matches,
                reason=(
                    "Human approval policy matched."
                ),
                confidence=1.0,
            )

        if "ALLOW" in outcomes:

            return PolicyEvaluation(
                permitted=True,
                approval_required=False,
                matched_policy_ids=matches,
                reason=(
                    "Explicit ALLOW policy matched."
                ),
                confidence=1.0,
            )

        # Fail safe when no policy matches.
        return PolicyEvaluation(
            permitted=False,
            approval_required=True,
            matched_policy_ids=[],
            reason=(
                "No explicit policy matched; "
                "fail safe."
            ),
            confidence=1.0,
        )