from domain.models import (
    Incident,
    IncidentDecision,
    RiskAssessment,
)


class RiskAnalyzer:

    def evaluate_risk(
        self,
        incident: Incident,
        decision: IncidentDecision,
        action: str,
    ) -> RiskAssessment:

        score = 0.0
        reasons = []

        if incident.environment == "production":

            score += 0.30
            reasons.append(
                "Production environment."
            )

        severity_scores = {
            "P1": 0.35,
            "P2": 0.20,
            "P3": 0.10,
            "P4": 0.05,
        }

        score += severity_scores.get(
            incident.severity,
            0.20,
        )

        reasons.append(
            f"Severity {incident.severity}."
        )

        if action in {
            "restart_server",
            "rollback_deployment",
        }:

            score += 0.20

            reasons.append(
                f"State-changing action: {action}."
            )

        score += max(
            0.0,
            0.20 * (
                1.0 - decision.confidence
            ),
        )

        if decision.confidence < 0.8:

            reasons.append(
                "Decision confidence is below 0.80."
            )

        score = min(score, 1.0)

        if score >= 0.80:
            level = "CRITICAL"

        elif score >= 0.60:
            level = "HIGH"

        elif score >= 0.35:
            level = "MEDIUM"

        else:
            level = "LOW"

        return RiskAssessment(
            risk_score=score,
            risk_level=level,
            reasons=reasons,
        )