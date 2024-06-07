from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from Auth.Utils import generate_password, validate_password
from Db.Orms.UserOrm import UserOrm
from Db.core import session_maker
from Schemas.Auth.SignInUser import SignInUser
from Schemas.Auth.SignUpUser import SignUpUser
from Schemas.UserDTO import UserDTO


async def create_user(user: SignUpUser) -> UserDTO:
    async with session_maker.begin() as session:
        user.password = generate_password(user.password).decode("utf-8")
        user_orm: UserOrm = UserOrm(username=user.username, password=user.password, email=user.email, wallets=[])
        session.add(user_orm)
        try:
            await session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exist")
        dto = UserDTO.model_validate(user_orm, from_attributes=True)
        return dto


async def get_user_by_id(id: int) -> UserDTO:
    async with session_maker.begin() as session:
        user: UserOrm = await session.execute(
            select(UserOrm).options(selectinload(UserOrm.wallets)).where(UserOrm.id == id))
        user = user.scalar()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDTO.model_validate(user, from_attributes=True)


async def get_user_by_email(email: str) -> UserDTO:
    async with session_maker.begin() as session:
        user: UserOrm = await session.execute(
            select(UserOrm).options(selectinload(UserOrm.wallets)).where(UserOrm.email == email))
        user = user.scalar()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDTO.model_validate(user, from_attributes=True)


async def SignIn(user: SignInUser):
    userDto: UserDTO = await get_user_by_email(user.email)
    if validate_password(user.password, userDto.password.encode("utf-8")):
        return userDto
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid data")
