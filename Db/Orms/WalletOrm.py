from datetime import datetime
from decimal import Decimal

from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Db.Orms.UserOrm import UserOrm
from Db.core import Base
from Schemas.Transfers.WalletSchema import CurrencyEnum


class WalletOrm(Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(50))
    currency: Mapped[CurrencyEnum] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(default=Decimal(0))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    owner: Mapped[UserOrm] = relationship(
        back_populates="wallets",
        cascade="save-update,merge"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
