from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select, or_

from Db.Orms.TransferOrm import TransferOrm
from Db.Orms.WalletOrm import WalletOrm
from Db.core import session_maker
from Db.utils import check_amount, check_currencies, exchange_rates
from Schemas.Transfers.TransferSchema import AddTransferSchema, TransferSchema


async def make_transfer(wallet_id, addTransfer: AddTransferSchema, user_id) -> TransferSchema:
    async with session_maker.begin() as session:
        from_wallet = await session.get(WalletOrm, wallet_id)
        to_wallet = await session.get(WalletOrm, addTransfer.to_wallet_id)
        transfer = TransferOrm(from_user_id=user_id, amount=addTransfer.amount,
                               to_user_id=addTransfer.to_user_id,
                               from_wallet_id=wallet_id,
                               to_wallet_id=to_wallet.id)
        if check_amount(from_wallet.amount, addTransfer.amount):
            if check_currencies(from_wallet.currency, to_wallet.currency):
                transfer.currency = to_wallet.currency
                from_wallet.amount -= addTransfer.amount
                to_wallet.amount += addTransfer.amount
            for key in exchange_rates.keys():
                if key[4:] == to_wallet.currency and key[:3] == from_wallet.currency:
                    from_wallet.amount -= addTransfer.amount
                    transfer.currency = key
                    to_wallet.amount += addTransfer.amount * Decimal(exchange_rates[key])
            session.add(transfer)
            session.refresh(from_wallet)
            session.refresh(to_wallet)
            await session.commit()
            return TransferSchema.model_validate(transfer, from_attributes=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You dont have enough money for transfer")


async def get_transfers(user_id: int) -> list[TransferSchema]:
    async with session_maker.begin() as session:
        res = await session.execute(
            select(TransferOrm).where(or_(TransferOrm.to_user_id == user_id, TransferOrm.from_user_id == user_id)))
        return [TransferSchema.model_validate(row, from_attributes=True) for row in res.scalars().all()]
