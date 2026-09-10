from domain.models import (
    ExecutionRoute,
    Incident,
    PolicyEvaluation,
    RiskAssessment,
)


class ActionAuthorization:

    def authorize(
        self,
        incident: Incident,
        action: str,
        risk: RiskAssessment,
        policy: PolicyEvaluation,
    ) -> ExecutionRoute:

        if not policy.permitted:

            return ExecutionRoute(
                mode="REJECT",
                executor=None,
                reason=policy.reason,
            )

        if (
            policy.approval_required
            or risk.risk_level == "CRITICAL"
        ):

            return ExecutionRoute(
                mode="HITL",
                executor=self._executor_for(action),
                reason=(
                    "Human approval required."
                ),
            )

        executor = self._executor_for(action)

        if executor is None:

            return ExecutionRoute(
                mode="REJECT",
                executor=None,
                reason=(
                    f"No executor registered "
                    f"for {action}."
                ),
            )

        return ExecutionRoute(
            mode="AUTOMATED",
            executor=executor,
            reason=(
                "Policy permits automated execution."
            ),
        )

    @staticmethod
    def _executor_for(
        action: str,
    ) -> str | None:

        return {
            "restart_server": "server_restart",
        }.get(action)