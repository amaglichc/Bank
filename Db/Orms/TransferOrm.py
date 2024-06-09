from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from Db.core import Base
from Schemas.Transfers.WalletSchema import CurrencyEnum


class TransferOrm(Base):
    __tablename__ = "transfers"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    from_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    amount: Mapped[Decimal] = mapped_column()
    currency: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
