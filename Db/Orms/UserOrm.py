from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Db.core import Base
from Schemas.UserDTO import RoleEnum

if TYPE_CHECKING:
    from Db.Orms.WalletOrm import WalletOrm


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, server_default=RoleEnum.user, default=RoleEnum.user)
    wallets: Mapped[list["WalletOrm"]] = relationship(
        back_populates="owner",
        lazy="selectin",
        cascade="save-update, merge"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
