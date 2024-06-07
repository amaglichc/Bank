from sqlalchemy import select

from Db.Orms.WalletOrm import WalletOrm
from Db.core import session_maker
from Schemas.Transfers.WalletSchema import AddWalletSchema, WalletSchema


async def create_wallet(wallet: AddWalletSchema) -> WalletSchema:
    async with session_maker.begin() as session:
        wallet_orm: WalletOrm = WalletOrm(name=wallet.name, currency=wallet.currency, amount=0,
                                          owner_id=wallet.owner_id)
        session.add(wallet_orm)
        await session.commit()
        return WalletSchema.model_validate(wallet_orm, from_attributes=True)


async def get_client_wallets(client_id: int) -> list[WalletSchema]:
    async with session_maker.begin() as session:
        wallets = await session.execute(select(WalletOrm).where(WalletOrm.owner_id == client_id))
        return [WalletSchema.model_validate(wallet, from_attributes=True) for wallet in wallets.scalars().all()]
