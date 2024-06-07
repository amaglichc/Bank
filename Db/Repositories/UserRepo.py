from fastapi import HTTPException, status
from sqlalchemy import select

from Auth.Utils import generate_password, validate_password
from Db.Orms.UserOrm import UserOrm
from Db.core import session_maker
from Schemas.Auth.SignInUser import SignInUser
from Schemas.Auth.SignUpUser import SignUpUser
from Schemas.UserDTO import UserDTO


async def create_user(user: SignUpUser) -> UserDTO:
    async with session_maker.begin() as session:
        user.password = generate_password(user.password).decode("utf-8")
        user_orm: UserOrm = UserOrm(username=user.username, password=user.password, email=user.email)
        session.add(user_orm)
        await session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


async def get_user_by_id(id: int) -> UserDTO:
    async with session_maker.begin() as session:
        user: UserOrm = await session.get(UserOrm, id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDTO.model_validate(user, from_attributes=True)


async def get_user_by_email(email: str) -> UserDTO:
    async with session_maker.begin() as session:
        user: UserOrm = await session.execute(select(UserOrm).where(UserOrm.email == email))
        return UserDTO.model_validate(user.scalar(), from_attributes=True)


async def SignIn(user: SignInUser):
    async with session_maker.begin() as session:
        userDto: UserDTO = await get_user_by_email(user.email)
        if validate_password(user.password, userDto.password.encode("utf-8")):
            return userDto
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid data")
