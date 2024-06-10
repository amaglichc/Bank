from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from Auth.JWT.jwt import decode_jwt
from Db.Repositories import UserRepo, WalletRepo
from Schemas.Transfers.WalletSchema import WalletSchema
from Schemas.UserSchema import UserDTO, RoleEnum

bearer = HTTPBearer()


def get_token_payload(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    try:
        payload = decode_jwt(token=cred.credentials)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return payload


def check_token_type(payload: Annotated[dict, Depends(get_token_payload)]):
    if payload["type"] == "access":
        return payload
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid token type"
    )


async def get_current_user(payload: dict) -> UserDTO:
    user: UserDTO = await UserRepo.get_user_by_id(payload.get("id"))
    return user


async def check_wallet_access(wallet_id: int, payload: dict) -> bool:
    wallet: WalletSchema = await WalletRepo.get_wallet_by_id(wallet_id)
    if wallet.owner_id == payload["sub"] or payload["role"] == RoleEnum.admin:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have access to this resource")


async def check_user_access(user_id: int, payload: dict) -> bool:
    if user_id == payload["sub"] or payload["role"] == RoleEnum.admin:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have access to this resource")
