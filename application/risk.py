from domain.models import (
    ActionRequest,
    Incident,
    IncidentDecision,
    RiskAssessment,
)


class RiskAnalyzer:

    async def evaluate_risk(
        self,
        incident: Incident,
        decision: IncidentDecision,
        action: ActionRequest,
    ) -> RiskAssessment:

        score = 0.0
        reasons: list[str] = []

        # Environment
        if incident.environment == "production":
            score += 0.25
            reasons.append(
                "Action targets production."
            )

        # Severity
        severity_scores = {
            "P1": 0.30,
            "P2": 0.20,
            "P3": 0.10,
            "P4": 0.05,
        }

        severity_score = severity_scores.get(
            incident.severity,
            0.10,
        )

        score += severity_score

        reasons.append(
            f"Incident severity: {incident.severity}"
        )

        # Action risk
        action_scores = {
            "restart_server": 0.20,
            "rollback_deployment": 0.25,
            "update_database": 0.40,
            "delete_data": 0.50,
        }

        action_score = action_scores.get(
            action.action,
            0.20,
        )

        score += action_score

        reasons.append(
            f"Action risk: {action.action}"
        )

        # Low confidence increases risk.
        if decision.confidence < 0.80:

            score += 0.15

            reasons.append(
                "Incident decision has relatively "
                "low confidence."
            )

        score = min(score, 1.0)

        if score >= 0.80:
            level = "CRITICAL"
        elif score >= 0.60:
            level = "HIGH"
        elif score >= 0.30:
            level = "MEDIUM"
        else:
            level = "LOW"

        return RiskAssessment(
            risk_score=score,
            risk_level=level,
            reasons=reasons,
        )