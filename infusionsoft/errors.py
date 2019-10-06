
class InfusionsoftException(Exception):
    """Base exception for all library errors."""
    pass


class AuthError(InfusionsoftException):
    """Something is wrong with authentication."""
    pass


class TokenError(AuthError):
    """Something is wrong with the tokens."""
    pass


class DataError(InfusionsoftException, ValueError):
    """Something is wrong with the data."""
    pass


class ConnectionError(InfusionsoftException, ConnectionError):
    """Something is wrong with the connection."""
    pass
