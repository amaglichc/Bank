from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from Auth.JWT.Security import bearer
from Auth.JWT.jwt import get_jwt, refresh_jwt
from Db.Repositories import UserRepo
from Schemas.Auth.SignInUser import SignInUser
from Schemas.Auth.SignUpUser import SignUpUser
from Schemas.Auth.Token import TokenInfo
from Schemas.UserSchema import UserDTO

router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def signUp(user: SignUpUser) -> UserDTO:
    return await UserRepo.create_user(user)


@router.post("/sign-in", status_code=status.HTTP_200_OK)
async def signIn(user: SignInUser) -> TokenInfo:
    user_dto = await UserRepo.SignIn(user)
    tokens = await get_jwt(user_dto)
    return tokens


@router.get("", status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int) -> UserDTO:
    return await UserRepo.get_user_by_id(id)


@router.post("/refresh")
async def refresh_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> TokenInfo:
    return await refresh_jwt(credentials.credentials)

# @router.post("/sign-in", status_code=status.HTTP_200_OK)
# async def signIn(use: SignInUser) -> TokenInfo:
#     pass
