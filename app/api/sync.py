from fastapi import APIRouter, Depends
from app.usecases.sync import SyncUsecase
from app.deps import get_sync_usecase

router = APIRouter()


@router.post("/sync/trigger", status_code=200)
async def trigger_sync(
    usecase: SyncUsecase = Depends(get_sync_usecase),
):
    await usecase.trigger()
    return {"status": "ok"}
