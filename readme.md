# Incident AI - Agentic Incident Response Practice

A local production-oriented architecture exercise for an AI incident-response system.

## Current Flow

Alert / Incident
→ Planner
→ ExecutionPlan
→ Scheduler
→ Worker Registry
→ Parallel Workers
→ Evidence Aggregator
→ Hypothesis Generator
→ Investigation Assessment

If evidence is insufficient:
→ Planner investigates again

If evidence is sufficient:
→ Incident Decision
→ Risk Assessment
→ Policy Evaluation
→ Authorization
→ HITL / Automated Execution
→ Verification
→ Bounded Retry / Investigation Loop

## Run

Python 3.11+

```bash
python -m venv .venv