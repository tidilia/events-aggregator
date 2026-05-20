from fastapi import APIRouter, Depends
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.deps import get_metrics_service
from app.services.metrics import MetricsService

metrics_router = APIRouter()


@metrics_router.get("/metrics")
async def metrics(service: MetricsService = Depends(get_metrics_service)):
    await service.update_business_metrics()

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
