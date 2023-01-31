from abc import ABC, abstractmethod

from app.core import Context
from app.domain import entities


class Users(ABC):
    @abstractmethod
    async def insert(self, ctx: Context, user: entities.User):
        """Add user to database"""
