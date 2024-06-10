import bcrypt
from fastapi import HTTPException, status

from Db.Repositories import WalletRepo
from Schemas.Transfers.TransferSchema import AddTransferSchema


def generate_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_pw = password.encode("utf-8")
    return bcrypt.hashpw(password=bytes_pw, salt=salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password)


async def validate_access(wallet_id: int, transfer: AddTransferSchema, payload: dict) -> bool:
    wallet_from = await WalletRepo.get_wallet_by_id(wallet_id)
    wallet_to = await WalletRepo.get_wallet_by_id(transfer.to_wallet_id)
    if wallet_from.owner_id == payload["sub"] and wallet_to.owner_id == transfer.to_user_id:
        return True
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
