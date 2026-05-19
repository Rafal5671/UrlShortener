import random
import string
from urllib.parse import urlparse

from app.extensions import db
from app.models.url import ShortURL


class URLValidationError(ValueError):
    """Raised when the provided URL is invalid."""


class URLNotFoundError(LookupError):
    """Raised when a short code does not exist in the database."""


class URLService:
    def __init__(self, short_code_length: int = 6) -> None:
        self._short_code_length = short_code_length

    def shorten(self, original_url: str) -> tuple[ShortURL, bool]:
        """
        Shorten a URL. Returns (ShortURL, created) where created is True
        if a new record was inserted, False if it already existed.
        Raises URLValidationError if the URL is invalid.
        """
        url = original_url.strip()
        self._validate_url(url)

        existing = ShortURL.query.filter_by(original_url=url).first()
        if existing:
            return existing, False

        code = self._generate_unique_code()
        entry = ShortURL(original_url=url, short_code=code)
        db.session.add(entry)
        db.session.commit()
        return entry, True

    def get_by_code(self, short_code: str) -> ShortURL:
        """
        Look up a record by its short code.
        Raises URLNotFoundError if the code does not exist.
        """
        entry = ShortURL.query.filter_by(short_code=short_code).first()
        if not entry:
            raise URLNotFoundError(f"Short code not found: {short_code!r}")
        return entry

    def _validate_url(self, url: str) -> None:
        """Raise URLValidationError if the URL has no valid scheme or domain."""
        if not url:
            raise URLValidationError("URL must not be empty.")
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise URLValidationError("URL must start with http:// or https://")
        if not parsed.netloc:
            raise URLValidationError("URL must contain a domain.")

    def _generate_unique_code(self) -> str:
        """Generate a random alphanumeric code that does not yet exist in the database."""
        chars = string.ascii_letters + string.digits
        while True:
            code = "".join(random.choices(chars, k=self._short_code_length))
            if not ShortURL.query.filter_by(short_code=code).first():
                return code
