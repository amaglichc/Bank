from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr

from Schemas.Transfers.TransferSchema import TransferSchema
from Schemas.Transfers.WalletSchema import WalletSchema


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class UserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    role: RoleEnum
    created_at: datetime
    wallets: list[WalletSchema] = []
