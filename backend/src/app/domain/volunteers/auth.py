from __future__ import annotations

import time
from uuid import UUID

import msgspec
from msgspec import Struct
from authlib.jose import jwt, JWTClaims
from litestar import Response, Request

from app.server import get_settings
from app.exceptions import ForbiddenError
from app.domain.volunteers.exceptions import (
    TokenMissingError,
    TokenInvalidError,
)


class Claims(Struct):
    sub: UUID
    exp: int
    iat: int
    scope: str


JWT_LIFETIME = 3600


def create_claims(account_id: UUID) -> Claims:
    scope_list = []

    # Add scopes here

    scope_string = " ".join(scope_list)

    now = int(time.time())

    claims = Claims(
        sub=account_id,
        exp=now + JWT_LIFETIME,
        iat=now,
        scope=scope_string,
    )

    return claims


def issue_registration_token(email: str, credentials_id: UUID) -> str:
    header = {"alg": "HS256"}
    settings = get_settings()
    secret = settings.api.jwt_secret_key
    now = int(time.time())
    payload = {
        "email": email,
        "credentials_id": str(credentials_id),
        "exp": now + (60 * 60 * 24),  # 1 day
        "iat": now,
    }
    token = jwt.encode(header, payload, secret).decode("utf-8")
    return token


def check_registration_token(token: str):
    settings = get_settings()
    secret = settings.api.jwt_secret_key

    try:
        payload = jwt.decode(token, secret)
        payload.validate(leeway=5)
        email = payload["email"]
        credentials_id = payload["credentials_id"]
        return email, UUID(credentials_id)
    except:
        raise ForbiddenError()


def issue_token(claims: Claims) -> str:
    header = {"alg": "HS256"}
    settings = get_settings()
    secret = settings.api.jwt_secret_key
    payload = msgspec.to_builtins(claims, builtin_types=(str, int))
    token = jwt.encode(header, payload, secret).decode("utf-8")
    print(token, type(token))
    return token


def decode_token(token: str) -> Claims | None:
    settings = get_settings()
    secret = settings.api.jwt_secret_key
    
    try:
        payload: JWTClaims = jwt.decode(token, secret)
        payload.validate(leeway=5)
        return msgspec.convert(payload, Claims)
    except:
        return None


def get_claims_from_token(
    token: str | None,
) -> Claims | None:
    if token is None:
        raise TokenMissingError()
    
    claims = decode_token(token)
    
    if not claims:
        raise TokenInvalidError()
    
    return claims


def get_claims_from_cookies(
    cookies: dict[str, str],
) -> Claims | None:
    token = get_token_from_cookies(cookies)
    return get_claims_from_token(token)


def set_auth_cookie(
    response: Response,
    token: str,
    key: str = "Auth",
) -> None:
    settings = get_settings()
    _400_DAYS = 400 * 24 * 60 * 60

    if settings.api.debug:
        response.set_cookie(
            key=key,
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=_400_DAYS,
        )
    else:
        response.set_cookie(
            key=f"__Secure-{key}",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=_400_DAYS,
        )


def delete_auth_cookie(
    response: Response,
    key: str = "Auth",
) -> None:
    settings = get_settings()

    response.delete_cookie(key, path="/")

    if settings.api.debug:
        return

    response.set_cookie(
        key=f"__Secure-{key}",
        value="",
        max_age=0,
        expires=0,
        path="/",
        domain=None,
        secure=True,
        httponly=True,
        samesite="lax",
    )


def get_token_from_cookies(
    cookies: dict[str, str],
    key: str = "Auth",
) -> str | None:
    settings = get_settings()

    if settings.api.debug:
        return cookies.get(key)
    else:
        return cookies.get(f"__Secure-{key}")


def get_auth_cookie(
    request: Request,
    key: str = "Auth",
) -> str | None:
    return get_token_from_cookies(request.cookies, key)
