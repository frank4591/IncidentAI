from domain.models import (
    Evidence,
    Hypothesis,
    Incident,
)


class HypothesisGenerator:

    def generate(
        self,
        incident: Incident,
        evidence: list[Evidence],
    ) -> list[Hypothesis]:

        hypotheses = []

        categories = {
            e.category
            for e in evidence
        }

        if "DATABASE" in categories:

            hypotheses.append(
                Hypothesis(
                    hypothesis_id="H-DB",
                    statement=(
                        "Database connectivity or "
                        "connection-pool exhaustion "
                        "is causing the incident."
                    ),
                    supporting_evidence=[
                        e.evidence_id
                        for e in evidence
                        if e.category == "DATABASE"
                    ],
                    contradicting_evidence=[],
                    confidence=0.82,
                )
            )

        if "DEPLOYMENT" in categories:

            hypotheses.append(
                Hypothesis(
                    hypothesis_id="H-DEPLOY",
                    statement=(
                        "A recent deployment "
                        "introduced a regression."
                    ),
                    supporting_evidence=[
                        e.evidence_id
                        for e in evidence
                        if e.category == "DEPLOYMENT"
                    ],
                    contradicting_evidence=[],
                    confidence=0.75,
                )
            )

        if "INFRASTRUCTURE" in categories:

            hypotheses.append(
                Hypothesis(
                    hypothesis_id="H-INFRA",
                    statement=(
                        "An infrastructure failure "
                        "is causing the incident."
                    ),
                    supporting_evidence=[
                        e.evidence_id
                        for e in evidence
                        if e.category == "INFRASTRUCTURE"
                    ],
                    contradicting_evidence=[],
                    confidence=0.70,
                )
            )

        return hypotheses