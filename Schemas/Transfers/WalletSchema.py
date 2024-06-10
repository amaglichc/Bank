from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    usd = "usd"
    eur = "eur"
    jpy = "jpy"
    rub = "rub"
    gbp = "gbp"
    rub_usd = "rub_usd"
    rub_eur = "rub_eur"
    rub_jpy = "rub_jpy"
    rub_gbp = "rub_gbp"
    usd_rub = "usd_rub"
    usd_eur = "usd_eur"
    usd_jpy = "usd_jpy"
    usd_gbp = "usd_gbp"
    eur_usd = "eur_usd"
    eur_jpy = "eur_jpy"
    eur_gbp = "eur_gbp"
    eur_rub = "eur_rub"
    jpy_usd = "jpy_usd"
    jpy_eur = "jpy_eur"
    jpy_gbp = "jpy_gbp"
    jpy_rub = "jpy_rub"
    gbp_rub = "gbp_rub"
    gbp_eur = "gbp_eur"
    gbp_jpy = "gbp_jpy"
    gbp_usd = "gbp_usd"


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
