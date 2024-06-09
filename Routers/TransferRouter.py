from fastapi import APIRouter

from Schemas.Transfers.TransferSchema import AddTransferSchema, TransferSchema

router = APIRouter(
    prefix="/transfers",
    tags=["transfers", "sigma"]
)


