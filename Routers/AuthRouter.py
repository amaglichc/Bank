from fastapi import APIRouter, status

from Auth.JWT.jwt import get_jwt
from Db.Repositories import UserRepo
from Schemas.Auth.SignInUser import SignInUser
from Schemas.Auth.SignUpUser import SignUpUser
from Schemas.Auth.Token import TokenInfo
from Schemas.UserDTO import UserDTO


router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def signUp(user: SignUpUser) -> UserDTO:
    return await UserRepo.create_user(user)


@router.post("/sign-in", status_code=status.HTTP_200_OK)
async def signIn(user: SignInUser) -> TokenInfo:
    tokens = await get_jwt(user)
    return tokens


@router.get("", status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int) -> UserDTO:
    return await UserRepo.get_user_by_id(id)

# @router.post("/sign-in", status_code=status.HTTP_200_OK)
# async def signIn(use: SignInUser) -> TokenInfo:
#     pass
