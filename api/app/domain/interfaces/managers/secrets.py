from abc import ABC, abstractmethod

from app.core import Context


class Secrets(ABC):
    @abstractmethod
    async def encrypt(self, ctx: Context, pwd: str) -> str:
        """Simple encrypt password for storage."""
