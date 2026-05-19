from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.url import ShortURL


@dataclass(frozen=True)
class ShortURLResponse:
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: str

    @classmethod
    def from_model(cls, model: "ShortURL", base_url: str) -> "ShortURLResponse":
        return cls(
            id=model.id,
            original_url=model.original_url,
            short_code=model.short_code,
            short_url=f"{base_url.rstrip('/')}/{model.short_code}",
            created_at=model.created_at.isoformat(),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "short_url": self.short_url,
            "created_at": self.created_at,
        }
