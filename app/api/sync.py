from fastapi import APIRouter, Depends
from app.usecases.sync import SyncUsecase

router = APIRouter()


@router.post("/sync/trigger", status_code=200)
async def trigger_sync(usecase: SyncUsecase = Depends()):
    await usecase.trigger()
    return {"status": "ok"}
