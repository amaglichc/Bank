from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    uds = "usd"
    eur = "eur"
    jpy = "jpy"
    run = "rub"
    gbp = "gbp"


class AddWalletSchema(BaseModel):
    name: str | None = None
    owner_id: int
    currency: CurrencyEnum


class WalletSchema(AddWalletSchema):
    id: int
    amount: Decimal
    created_at: datetime
