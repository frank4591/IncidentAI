from domain.models import (
    Evidence,
    Hypothesis,
    Incident,
    InvestigationAssessment,
)


class InvestigationAssessor:

    def __init__(
        self,
        min_confidence: float = 0.75,
        min_evidence_count: int = 1,
    ):
        self.min_confidence = min_confidence
        self.min_evidence_count = min_evidence_count

    def assess(
        self,
        incident: Incident,
        evidence: list[Evidence],
        hypotheses: list[Hypothesis],
    ) -> InvestigationAssessment:

        if len(evidence) < self.min_evidence_count:

            return InvestigationAssessment(
                sufficient_evidence=False,
                confidence=0.0,
                competing_hypotheses=[],
                evidence_gaps=[
                    "More independent evidence is required."
                ],
                reason="Insufficient evidence count.",
            )

        ordered = sorted(
            hypotheses,
            key=lambda h: h.confidence,
            reverse=True,
        )

        competing = []

        if (
            len(ordered) >= 2
            and ordered[0].confidence
            - ordered[1].confidence <= 0.10
        ):
            competing = [
                ordered[0].hypothesis_id,
                ordered[1].hypothesis_id,
            ]

        confidence = (
            ordered[0].confidence
            if ordered
            else 0.0
        )

        sufficient = (
            confidence >= self.min_confidence
            and not competing
        )

        return InvestigationAssessment(
            sufficient_evidence=sufficient,
            confidence=confidence,
            competing_hypotheses=competing,
            evidence_gaps=(
                []
                if sufficient
                else [
                    "Resolve competing or "
                    "low-confidence hypotheses."
                ]
            ),
            reason=(
                "Evidence is sufficient."
                if sufficient
                else "Investigation requires more evidence."
            ),
        )