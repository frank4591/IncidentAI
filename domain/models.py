from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


IncidentStatus = Literal[
    "OPEN",
    "INVESTIGATING",
    "MITIGATING",
    "CLOSED",
]


@dataclass
class Incident:
    incident_id: str
    service: str
    alert_type: str
    severity: str
    environment: str
    started_at: datetime
    status: IncidentStatus = "OPEN"


@dataclass
class Evidence:
    evidence_id: str
    source: str
    category: str
    observation: str
    confidence: float
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Hypothesis:
    hypothesis_id: str
    statement: str
    supporting_evidence: list[str]
    contradicting_evidence: list[str]
    confidence: float
    evidence_gaps: list[str] = field(default_factory=list)


@dataclass
class IncidentDecision:
    incident_type: str
    accepted_hypotheses: list[str]
    rejected_hypotheses: list[str]
    reason: str
    confidence: float
    proposed_action: str


@dataclass
class ActionRequest:
    action: str
    target: str
    parameters: dict[str, Any]


@dataclass
class RiskAssessment:
    risk_score: float
    risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]
    reasons: list[str]


@dataclass
class PolicyRule:
    policy_id: str
    description: str
    conditions: dict[str, Any]
    outcome: Literal[
        "ALLOW",
        "HITL",
        "DENY",
    ]


@dataclass
class PolicyEvaluation:
    permitted: bool
    approval_required: bool
    matched_policy_ids: list[str]
    reason: str
    confidence: float


@dataclass
class ExecutionRoute:
    mode: Literal[
        "AUTOMATED",
        "HITL",
        "REJECT",
    ]
    executor: str | None
    reason: str


@dataclass
class ExecutionResult:
    action: str
    status: Literal[
        "SUCCESS",
        "FAILED",
        "TIMEOUT",
    ]
    attempt: int
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class VerificationResult:
    verified: bool
    service_healthy: bool
    alert_cleared: bool
    observations: list[str]
    reason: str


@dataclass
class WorkerTask:
    task_id: str
    capability: str
    parameters: dict[str, Any]
    priority: int = 1


@dataclass
class ExecutionPlan:
    plan_id: str
    iteration: int
    tasks: list[WorkerTask]
    reason: str


@dataclass
class WorkerResult:
    task_id: str
    worker_name: str
    status: Literal[
        "SUCCESS",
        "FAILED",
        "TIMEOUT",
    ]
    evidence: list[Evidence]
    error: str | None = None
    duration_ms: int | None = None


@dataclass
class InvestigationAssessment:
    sufficient_evidence: bool
    confidence: float
    competing_hypotheses: list[str]
    evidence_gaps: list[str]
    reason: str