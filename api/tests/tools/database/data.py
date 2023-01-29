from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypedDict


class Fixtures(ABC):
    @abstractmethod
    def with_folder(self, path: str) -> Fixtures:
        """Set path to folder holding fixture from base path"""

    @abstractmethod
    def with_base_path(self, path: str) -> Fixtures:
        """Set base path"""

    @abstractmethod
    def load_scripts(self) -> None:
        """Load all scripts in current fixture path"""

    @abstractmethod
    def load_script(self, name: str) -> Fixtures:
        """Load specified script only"""


class Request(ABC):
    @abstractmethod
    def table(self, name: str) -> Request:
        """Set table name"""

    @abstractmethod
    def with_id_field(self, id_fied: str) -> Request:
        """Set id field name"""

    @abstractmethod
    def with_condition(self, key: str, condition: Any, operator: str) -> Request:
        """Add condition to request"""

    @abstractmethod
    def with_fields(self, *fields: str) -> Request:
        """Add fields to use for request"""

    @abstractmethod
    def with_values(self, values: List[Any]) -> Request:
        """
        Add values for insert/update request.
        /!\\ values should match declared fields in exact order
        """

    @abstractmethod
    def with_mapped_data(self, data: Dict[str, Any]) -> Request:
        """
        Add data from dict for insert/update request
        """

    @abstractmethod
    def insert(self, ignore_error: bool = True) -> None:
        """Emit call as insert request"""

    @abstractmethod
    def update(self, ignore_error: bool = True) -> None:
        """Emit call as update request"""

    @abstractmethod
    def upsert(self, ignore_error: bool = True) -> None:
        """Emit call as upsert request"""

    @abstractmethod
    def delete(self, ignore_error: bool = True) -> None:
        """Emit call as delete request"""


class Asserts(ABC):
    class Matcher(TypedDict):
        field: str
        op: str
        value: Any

    @abstractmethod
    def exists(self, table: str, id_val: Any, id_field: str = "id") -> Dict:
        """
        Ensure entry exists with provided id.
        Return value as dict if exists.
        """

    @abstractmethod
    def exists_with_value(
        self,
        table: str,
        *matchers: Matcher,
        expect_one: bool = True,
        order_by: Dict[str, str] = None,
    ) -> Dict | List[Dict]:
        """
        Ensure value exists with matching conditions.
        Return value as dict/List[dict] if exists.
        """
