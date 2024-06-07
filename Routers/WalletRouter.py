from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, status, Depends

from Auth.JWT.Security import get_token_payload, check_wallet_access
from Db.Repositories import WalletRepo
from Schemas.Transfers.WalletSchema import WalletSchema, AddWalletSchema

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_wallet(wallet: AddWalletSchema, payload: Annotated[dict, Depends(get_token_payload)]) -> WalletSchema:
    return await WalletRepo.create_wallet(wallet, payload["sub"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_wallets_for_client(payload: Annotated[dict, Depends(get_token_payload)]) -> list[
    WalletSchema]:
    return await WalletRepo.get_client_wallets(payload["sub"])


# delete in the future
@router.post("/{wallet_id}", status_code=status.HTTP_200_OK)
async def replenis_wallet(wallet_id: int, amount: Decimal) -> WalletSchema:
    return await WalletRepo.replenish_amount(wallet_id, amount)


@router.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(wallet_id: int, payload: Annotated[dict, Depends(get_token_payload)],
                        to_wallet_id: int | None = None):
    if await check_wallet_access(wallet_id, payload):
        return await WalletRepo.delete_wallet(wallet_id, to_wallet_id)
