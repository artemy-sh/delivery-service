"""
Domain-level exceptions for business rule.
"""


class DomainError(Exception):
    """Base class for domain errors."""

    pass


class InvalidWeight(DomainError):
    """Raised when parcel weight is invalid."""

    pass


class InvalidParcelId(DomainError):
    """Raised when parcel ID is invalid."""

    pass


class InvalidUserId(DomainError):
    """Raised when user ID is invalid."""

    pass


class InvalidMoney(DomainError):
    """Raised when money value or currency is invalid."""

    pass


class InvalidExchangeRate(DomainError):
    """Raised when exchange rate is zero or negative."""

    pass


class DeliveryPriceAlreadySet(DomainError):
    """Raised when trying to set delivery price again."""

    pass
