from decimal import Decimal

from Schemas.Transfers.WalletSchema import CurrencyEnum


def check_amount(amount_on_wallet: Decimal, amount_to_transfer: Decimal) -> bool:
    return amount_on_wallet >= amount_to_transfer


def check_currencies(from_wallet_currency: CurrencyEnum, to_wallet_currency: CurrencyEnum) -> bool:
    return from_wallet_currency == to_wallet_currency


exchange_rates = {
    "rub_usd": 0.011,
    "rub_eur": 0.01,
    "rub_jpy": 0.57,
    "rub_gbp": 0.0088,
    "usd_rub": 89,
    "usd_eur": 0.93,
    "usd_jpy": 157.11,
    "usd_gbp": 0.79,
    "eur_usd": 1.08,
    "eur_jpy": 168.92,
    "eur_gbp": 0.85,
    "eur_rub": 95.7,
    "jpy_usd": 0.0064,
    "jpy_eur": 0.0059,
    "jpy_gbp": 0.005,
    "jpy_rub": 0.57,
    "gbp_rub": 113.12,
    "gbp_eur": 1.18,
    "gbp_jpy": 199.52,
    "gbp_usd": 1.27
}
