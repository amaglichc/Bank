from fastapi import APIRouter, status

from Db.Repositories import WalletRepo
from Schemas.Transfers.WalletSchema import WalletSchema, AddWalletSchema

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_wallet(wallet: AddWalletSchema) -> WalletSchema:
    return await WalletRepo.create_wallet(wallet)


@router.get("/{client_id}", status_code=status.HTTP_200_OK)
async def get_wallets_for_client(client_id: int) -> list[WalletSchema]:
    return await WalletRepo.get_client_wallets(client_id)
