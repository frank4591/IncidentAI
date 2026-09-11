from dataclasses import dataclass
from typing import Protocol

from domain.models import (
    Evidence,
    WorkerResult,
)


@dataclass
class EvidenceAssessment:

    evidence: list[Evidence]
    overall_confidence: float
    conflicts: list[str]
    coverage: float

class EviAggregator(Protocol):

    async def aggregate(
        self,
        worker_results: list[WorkerResult],
        existing_evidence: list[Evidence],
    ) -> list[Evidence]:
        ...

class EvidenceAggregator:

    def aggregate(
        self,
        worker_results: list[WorkerResult],
        existing_evidence: list[Evidence],
    ) -> EvidenceAssessment:

        evidence = list(existing_evidence)

        for result in worker_results:

            if result.status == "SUCCESS":
                evidence.extend(result.evidence)

        confidence = (
            sum(
                e.confidence
                for e in evidence
            ) / len(evidence)
            if evidence
            else 0.0
        )

        expected = {
            "DATABASE",
            "APPLICATION",
            "INFRASTRUCTURE",
            "DEPLOYMENT",
        }

        observed = {
            e.category
            for e in evidence
        }

        coverage = (
            len(expected & observed)
            / len(expected)
        )

        return EvidenceAssessment(
            evidence=evidence,
            overall_confidence=confidence,
            conflicts=[],
            coverage=coverage,
        )