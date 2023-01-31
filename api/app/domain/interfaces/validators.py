from abc import ABC, abstractmethod

from app.core import Context
from app.domain import entities


class Users(ABC):
    @abstractmethod
    async def register(self, ctx: Context, user: entities.User, clear_password: str):
        """Check if user is valid for registration"""
