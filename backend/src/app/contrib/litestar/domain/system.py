from __future__ import annotations

from litestar import Controller, get


class HealthController(Controller):
    path = "/health"
    tags = ["Health"]


    @get("/liveness", operation_id="HealthLivenessCheck")
    async def health_liveness_check(self) -> None:
        pass


    @get("/readiness", operation_id="HealthReadinessCheck")
    async def health_readiness_check(self) -> None:
        pass
