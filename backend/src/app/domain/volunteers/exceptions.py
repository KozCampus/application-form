from __future__ import annotations

from app.exceptions import (
    Error,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


class TokenMissingError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """No authentication token was sent to the server."""


class TokenInvalidError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided authentication token is invalid."""


class AccountNotFoundError(Error, status_code=HTTP_404_NOT_FOUND):
    """The requested account was not found."""


class InvalidPasswordError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided password is invalid."""


class InactiveAccountError(Error, status_code=HTTP_403_FORBIDDEN):
    """The requested account is inactive."""
