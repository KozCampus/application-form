from __future__ import annotations

import typing as t
import random
import secrets
from urllib.parse import urlencode

import httpx
from litestar.middleware.rate_limit import RateLimitConfig

from app.server import get_settings
from app.domain.volunteers.auth import (
    Claims,
    create_claims,
    issue_token,
    issue_registration_token,
)

from app.contrib.litestar import *  # type: ignore
from app.exceptions import ForbiddenError
from app.domain.volunteers.auth import (
    set_auth_cookie,
    delete_auth_cookie,
    issue_token,
)
from app.domain.volunteers.services import (
    AccountService,
    OAuth2CredentialsService,
)


auth_minute_rate_limit = RateLimitConfig(("minute", 60))
auth_daily_rate_limit = RateLimitConfig(("day", 600))


class AuthController(Controller):
    path = "/auth"
    tags = ["Auth"]
    middleware = [
        auth_minute_rate_limit.middleware,
        auth_daily_rate_limit.middleware,
    ]


    @get(
        operation_id="GetClientClaims",
        path="/claims",
    )
    async def get_client_claims(
        self,
        claims: Claims | None,
    ) -> Claims | None:
        return claims
    

    @get(
        operation_id="Redirect",
        path="/redirect",
    )
    async def redirect(self) -> Response:
        state = secrets.token_urlsafe(32)

        settings = get_settings()

        uri = urlencode({
            "client_id": settings.sso.google.client_id,
            "response_type": "code",
            "scope": "openid email https://www.googleapis.com/auth/calendar.events",
            "redirect_uri": f"{settings.api.base_url}/auth/callback",
            "state": state,
            "nonce": random.randint(0, 2**32),
        })

        response = Redirect(path=f"https://accounts.google.com/o/oauth2/v2/auth?{uri}")

        response.set_cookie(
            key="state",
            value=state,
            max_age=400 * 24 * 3600, # 400 days
            httponly=True,
            samesite="none",
            secure=True,
        )

        return response
    

    @get(
        path="/callback",
        operation_id="Callback",
    )
    async def callback(
        self,
        request: Request,
        code: str,
        state_: t.Annotated[str, Parameter(query="state")],
        account_service: AccountService,
        oauth2_credentials_service: OAuth2CredentialsService,
        db_session: AsyncSession,
    ) -> Response:
        if state_ != request.cookies.get("state"):
            raise ForbiddenError()

        settings = get_settings()

        # exchange code for token
        uri = urlencode({
            "code": code,
            "client_id": settings.sso.google.client_id,
            "client_secret": settings.sso.google.client_secret,
            "redirect_uri": f"{settings.api.base_url}/auth/callback",
            "grant_type": "authorization_code",
            "access_type": "offline",
            "prompt": "consent",
        })

        async with httpx.AsyncClient() as client:
            r = await client.post(f"https://oauth2.googleapis.com/token?{uri}")

        if r.status_code != 200:
            raise ForbiddenError()

        print(r.json())
        access_token = r.json()["access_token"]
        id_token = r.json()["id_token"]

        """ async with httpx.AsyncClient() as client:
            r = await client.get("https://www.googleapis.com/oauth2/v3/certs") """

        """ if r.status_code != 200:
            raise ForbiddenError()
        
        jwks = r.json() """

        #id_token_payload = jwt.decode(id_token, jwks) # type: ignore

        # get user info
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if r.status_code != 200:
            raise ForbiddenError()

        user_info = r.json()

        account = await account_service.get_one_or_none(
            email=user_info["email"],
        )

        credentials = await oauth2_credentials_service.create(
            data={
                "access_token": access_token,
            }
        )
        print(credentials)

        await db_session.commit()

        if account is not None:
            account.google_credentials_id = credentials.id
            print(credentials.id)
            print(account.google_credentials_id)
            claims = create_claims(account.id)
            token = issue_token(claims)
            response = Redirect(path=f"{settings.api.redirect_url}")
            set_auth_cookie(response, token)
            return response

        token = issue_registration_token(user_info["email"], credentials.id)
        response = Redirect(
            path=f"{settings.api.redirect_url}/signup?email={user_info['email']}"
        )

        set_auth_cookie(response, token, key="Reg")
        return response
    

    @post(
        operation_id="Logout",
        path="/logout",
    )
    async def logout(self) -> Response:
        response = Response(None)
        delete_auth_cookie(response, key="Auth")
        delete_auth_cookie(response, key="Reg")
        return response
