from typing import Any, Dict, List, Tuple

from click import UsageError
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from tests.config import DB_CONNECTION_STRING
from tests.tools import database


class Requests(database.Request):
    class Request(BaseModel):
        class Condition(BaseModel):
            field: str
            op: str
            value: Any

        table: str
        conditions: List[Condition] = []

        set_fields: Tuple[str, ...] = tuple()
        set_values: List[Dict[str, Any]] = []

        id_field: str = "id"

        def add_conditions(self, base) -> Tuple[str, Dict[str, Any]]:
            if not self.conditions:
                return base, {}

            base += " WHERE "
            args = {}
            for cond in self.conditions:
                base += f"{cond.field} {cond.op} :cond_{cond.field}"
                args["cond_" + cond.field] = cond.value

            return base, args

    __client: Engine = None  # type: ignore

    def __init__(self) -> None:
        if not Requests.__client:
            Requests.__client = create_engine(
                DB_CONNECTION_STRING,
                future=True,
                echo=True,
                pool_size=50,
                max_overflow=50,
                pool_pre_ping=True,
                pool_recycle=8 * 60,  # seconds
            )
        self.__request: Requests.Request

    def table(self, name: str) -> database.Request:
        self.__request = Requests.Request(table=name)

        return self

    def with_condition(self, key: str, condition: Any, operator: str) -> database.Request:
        self.__request.conditions.append(
            Requests.Request.Condition(field=key, op=operator, value=condition)
        )

        return self

    def with_id_field(self, id_fied: str) -> database.Request:
        self.__request.id_field = id_fied

        return self

    def with_fields(self, *fields: str) -> database.Request:
        self.__request.set_fields = fields

        return self

    def with_values(self, values: List[Any]) -> database.Request:
        to_add = {}
        for i, key in enumerate(self.__request.set_fields):
            to_add[key] = values[i]

        self.__request.set_values.append(to_add)

        return self

    def with_mapped_data(self, data: Dict[str, Any]) -> database.Request:
        keys = list(data.keys())

        for key in self.__request.set_fields:
            if key not in keys:
                data[key] = None
                keys.remove(key)

        for key in keys:
            if key not in self.__request.set_fields:
                self.__request.set_fields += (key,)

        self.__request.set_values.append(data)

        return self

    def insert(self, ignore_error: bool = True) -> None:
        if not self.__request:
            raise UsageError("InsertingWithoutRequestDefinition")

        base = f"INSERT INTO {self.__request.table} {self.__request.set_fields} VALUES (".replace(
            "'", ""
        )

        for field in self.__request.set_fields:
            base += f":{field}, "

        base = text(base.rstrip(", ") + ")")

        with self.__client.connect() as con:
            try:
                for insertable in self.__request.set_values:
                    con.execute(base, insertable)
                con.commit()
            except Exception as e:
                print(e)
                if not ignore_error:
                    raise e
            finally:
                con.close()

    def update(self, ignore_error: bool = True) -> None:
        if not self.__request:
            raise UsageError("UpdatingWithoutRequestDefinition")

        base = f"UPDATE {self.__request.table} SET "

        for field in self.__request.set_fields:
            base += f"{field} = :{field}, "

        base = base.rstrip(", ")

        base, cond = self.__request.add_conditions(base)
        base = text(base)

        with self.__client.connect() as con:
            try:
                for insertable in self.__request.set_values:
                    insertable.update(cond)
                    con.execute(base, insertable)

                con.commit()

            except Exception as e:
                print(e)
                if not ignore_error:
                    raise e
            finally:
                con.close()

    def upsert(self, ignore_error: bool = True) -> None:
        raise NotImplementedError("NotDoneYet")

    def delete(self, ignore_error: bool = True) -> None:
        if not self.__request:
            raise UsageError("DeletingWithoutRequestDefinition")

        base = f"DELETE FROM {self.__request.table} "

        base, cond = self.__request.add_conditions(base)
        base = text(base)

        with self.__client.connect() as con:
            try:
                con.execute(base, cond)

                con.commit()
            except Exception as e:
                print(e)
                if not ignore_error:
                    raise e
            finally:
                con.close()
