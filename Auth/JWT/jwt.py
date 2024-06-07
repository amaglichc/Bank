from datetime import datetime, UTC, timedelta
from pathlib import Path

import jwt
from Db.Repositories.UserRepo import SignIn
from Schemas.Auth.SignInUser import SignInUser
from Schemas.Auth.Token import TokenInfo

cwd = Path.cwd()
private_key_path: Path = cwd / 'keys' / 'jwt-private.pem'
public_key_path: Path = cwd / 'keys' / 'jwt-public.pem'


def encode_jwt(payload: dict, expire_minutes: int, algorithm: str = "RS256",
               key: str = private_key_path.read_text()) -> str:
    payload["iat"] = datetime.now(UTC)
    payload["exp"] = datetime.now(UTC) + timedelta(minutes=expire_minutes)
    return jwt.encode(payload, key, algorithm)


def decode_jwt(token: str,
               public_key: str = public_key_path.read_text(),
               algorithm: str = "RS256") -> dict:
    return jwt.decode(token, public_key, algorithm)


async def get_jwt(user: SignInUser):
    user_dto = await SignIn(user)
    access = encode_jwt({"type": "access", "sub": user_dto.id, "role": user_dto.role}, expire_minutes=180)
    refresh = encode_jwt({"type": "refresh", "sub": user_dto.id}, expire_minutes=60 * 24 * 30)
    return TokenInfo(access_token=access, refresh_token=refresh)
