from typing import Annotated

from fastapi import APIRouter, Depends

from Auth.JWT.Security import check_token_type
from Db.Repositories import TransferRepo
from Schemas.Transfers.TransferSchema import TransferSchema

router = APIRouter(
    prefix="/transfers",
    tags=["transfers"]
)


@router.get("")
async def get_transfers(payload: Annotated[dict, Depends(check_token_type)]) -> list[TransferSchema]:
    return await TransferRepo.get_transfers(payload["sub"])
