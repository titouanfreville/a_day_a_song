from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Transactions(ABC):
    """
    Transaction interface abstract transaction management
    to uniformise calls for different requirements
    """

    class ErrNoTransaction(Exception):
        def __init__(self, prefix: str = ""):
            if prefix:
                prefix += ": "
            super().__init__(prefix + "no transaction in progress")

    class ErrCommitted(Exception):
        def __init__(self, prefix: str = ""):
            super().__init__(prefix + "transaction was committed")

    class ErrRollbacked(Exception):
        def __init__(self, prefix: str = ""):
            super().__init__(prefix + "transaction was rollbacked")

    class Instance(ABC):
        """
        Processing transaction instance
        """

        @abstractmethod
        async def commit(self) -> None:
            """Commit transaction to storage"""

        @abstractmethod
        async def rollback(self) -> None:
            """Rollback cancel transaction"""

        @abstractmethod
        async def clear(self) -> None:
            """Fully reset transaction instance"""

        @abstractmethod
        def instance(self) -> Any:
            """Provide concrete transaction instance to user"""

        @abstractmethod
        async def __enter__(self) -> Transactions:
            """Define context enter sequence"""

        @abstractmethod
        async def __exit__(self) -> None:
            """Define context out sequence"""

    @abstractmethod
    async def start(self) -> Instance:
        """
        Init a transaction instance.
        """
