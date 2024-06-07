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
    currency: CurrencyEnum


class DeleteWalletSchema(BaseModel):
    wallet_to_delete_id: int
    wallet_for_money: int | None



class WalletSchema(AddWalletSchema):
    id: int
    amount: Decimal
    created_at: datetime
    owner_id: int
