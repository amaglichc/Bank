from Db.Orms.TransferOrm import TransferOrm
from Db.Orms.WalletOrm import WalletOrm
from Db.core import session_maker
from Schemas.Transfers.TransferSchema import AddTransferSchema, TransferSchema


async def make_transfer(wallet_id, addTransfer: AddTransferSchema, user_id) -> TransferSchema:
    async with session_maker.begin() as session:
        from_wallet = await session.get(WalletOrm, wallet_id)
        to_wallet = await session.get(WalletOrm, addTransfer.to_wallet_id)
        transfer = TransferOrm(from_user_id=user_id, amount=addTransfer.amount, to_user_id=addTransfer.to_user_id,
                               currency=from_wallet.currency, from_wallet_id=wallet_id, to_wallet_id=to_wallet.id)
        from_wallet.amount -= addTransfer.amount
        to_wallet.amount += addTransfer.amount
        session.add(transfer)
        session.refresh(from_wallet)
        session.refresh(to_wallet)
        await session.commit()
        return TransferSchema.model_validate(transfer, from_attributes=True)
