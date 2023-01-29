from copy import deepcopy as copy
from typing import Any, Dict, List

from pydantic import BaseModel


class Entity(BaseModel):
    initial_values: dict

    def __init__(self, **data: Any) -> None:
        data["initial_values"] = copy(data)
        super().__init__(**data)

    def dict(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        skip_defaults: bool | None = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        if not exclude:
            exclude = {"initial_values"}

        else:
            if isinstance(exclude, set):
                exclude.add("initial_values")

        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def to_log(self) -> Dict:
        return self.dict(exclude={"initial_values"})

    def updated_fields(self) -> List[str]:
        modified_key: List[str] = []
        analysed_key: List[str] = []
        for key, value in self.dict(exclude_defaults=True).items():
            analysed_key.append(key)

            if key == "initial_values":
                continue

            if key not in self.initial_values:
                modified_key.append(key)
                continue

            initial_value = self.initial_values[key]
            if value == initial_value:
                continue

            if isinstance(value, dict) and initial_value:
                checked_keys = []
                str_checked_keys = []
                for k, v in value.items():
                    if str(k) not in initial_value or initial_value[str(k)] != v:
                        modified_key.append(key)
                        break

                    checked_keys.append(k)
                    str_checked_keys.append(str(k))

                checked_keys.sort()

                if hasattr(initial_value, "keys") and [
                    k
                    for k in initial_value.keys()
                    if k not in checked_keys and k not in str_checked_keys
                ]:
                    modified_key.append(key)
            else:
                modified_key.append(key)

        old_item = self.__class__(**self.initial_values)
        for key, initial_value in old_item.dict(exclude_defaults=True).items():
            if key in analysed_key:
                continue

            value = getattr(self, key)
            if value == initial_value:
                continue

            if isinstance(initial_value, dict) and value:
                checked_keys = []
                str_checked_keys = []
                for k, v in initial_value.items():
                    if str(k) not in value or value[str(k)] != v:
                        modified_key.append(key)
                        break

                    checked_keys.append(k)
                    str_checked_keys.append(str(k))

                checked_keys.sort()

                if hasattr(value, "keys") and [
                    k for k in value.keys() if k not in checked_keys and k not in str_checked_keys
                ]:
                    modified_key.append(key)

            else:
                modified_key.append(key)

        return list(set(modified_key))
