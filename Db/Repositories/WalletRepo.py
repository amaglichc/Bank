from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from starlette import status

from Db.Orms.WalletOrm import WalletOrm
from Db.Repositories import UserRepo
from Db.core import session_maker
from Schemas.Transfers.WalletSchema import AddWalletSchema, WalletSchema


async def create_wallet(wallet: AddWalletSchema, owner_id: int) -> WalletSchema:
    async with session_maker.begin() as session:
        person = await UserRepo.get_user_by_id(owner_id)
        if person is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        wallet_orm: WalletOrm = WalletOrm(name=wallet.name, currency=wallet.currency, amount=0,
                                          owner_id=owner_id)
        session.add(wallet_orm)
        await session.commit()
        return WalletSchema.model_validate(wallet_orm, from_attributes=True)


async def get_wallet_by_id(wallet_id: int) -> WalletSchema:
    async with session_maker.begin() as session:
        wallet: WalletOrm = await session.execute(
            select(WalletOrm).options(selectinload(WalletOrm.owner)).where(WalletOrm.id == wallet_id))
        wallet = wallet.scalar()
        return WalletSchema.model_validate(wallet, from_attributes=True)


async def replenish_amount(wallet_id: int, amount: Decimal) -> WalletSchema:
    async with session_maker.begin() as session:
        wallet_orm: WalletOrm = await session.get(WalletOrm, wallet_id)
        wallet_orm.amount += amount
        await session.commit()
        return WalletSchema.model_validate(wallet_orm, from_attributes=True)


async def get_client_wallets(client_id: int) -> list[WalletSchema]:
    async with session_maker.begin() as session:
        wallets = await session.execute(
            select(WalletOrm).options(selectinload(WalletOrm.owner)).where(WalletOrm.owner_id == client_id))
        wallets = wallets.scalars().all()
        return [WalletSchema.model_validate(wallet, from_attributes=True) for wallet in wallets]


async def delete_wallet(wallet_id: int, to_wallet_id: int | None) -> None:
    async with session_maker.begin() as session:
        wallet_to_delete: WalletOrm = await session.get(WalletOrm, wallet_id)
        if to_wallet_id is not None:
            new_wallet: WalletOrm = await session.get(WalletOrm, to_wallet_id)
            if new_wallet.currency == wallet_to_delete.currency:
                new_wallet.amount += wallet_to_delete.amount
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Different currencies")
        elif wallet_to_delete.amount != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Select a wallet to transfer money")
        await session.execute(delete(WalletOrm).where(WalletOrm.id == wallet_to_delete.id))
        await session.commit()


async def get_another_client_wallets(wallet_id) -> list[AddWalletSchema]:
    async with session_maker.begin() as session:
        wallets = await session.execute(
            select(WalletOrm).options(selectinload(WalletOrm.owner)).where(WalletOrm.owner_id == wallet_id))
        return [AddWalletSchema.model_validate(row, from_attributes=True) for row in wallets.scalars().all()]
