class PocketLMError(Exception):
    """Base error for the application."""


class RateLimitError(PocketLMError):
    """Raised when concurrency limits are exceeded."""


class TaskValidationError(PocketLMError):
    """Raised when request-level task validation fails."""
