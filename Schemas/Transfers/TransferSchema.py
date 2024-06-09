from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from Schemas.Transfers.WalletSchema import CurrencyEnum


class AddTransferSchema(BaseModel):
    to_wallet_id: int
    to_user_id: int
    amount: Decimal


class TransferSchema(AddTransferSchema):
    id: int
    from_user_id: int
    currency: CurrencyEnum
    created_at: datetime
