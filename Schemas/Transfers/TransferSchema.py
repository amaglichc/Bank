from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from Schemas.Transfers.WalletSchema import CurrencyEnum


class TransferSchema(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    amount: Decimal
    currency: CurrencyEnum
    created_at: datetime
