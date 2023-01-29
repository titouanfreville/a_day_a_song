from typing import Any, Dict, List

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from tests.config import DB_CONNECTION_STRING
from tests.tools import database


class Asserts(database.Asserts):
    __client: Engine = None  # type: ignore

    def __init__(self) -> None:
        if not Asserts.__client:
            Asserts.__client = create_engine(
                DB_CONNECTION_STRING,
                future=True,
                echo=True,
                pool_size=50,
                max_overflow=50,
                pool_pre_ping=True,
                pool_recycle=8 * 60,  # seconds
            )

    def exists(self, table: str, id_val: Any, id_key: str = "id") -> Dict:
        query = text(f"SELECT * FROM {table} WHERE {id_key} = :id LIMIT 1")  # nosec

        with self.__client.connect() as con:
            result = con.execute(query, {"id": id_val}).first()

            if not result:
                raise ValueError("NotFound")

            return result._asdict()

    def exists_with_value(
        self,
        table: str,
        *matchers: database.Asserts.Matcher,
        expect_one: bool = True,
        order_by: Dict[str, str] = None,
    ) -> Dict | List[Dict]:
        if not matchers:
            return []

        query = f"SELECT * FROM {table} WHERE "  # nosec
        params = {}
        is_first = True
        i = 0
        for matcher in matchers:
            params[str(i)] = matcher["value"]

            if not is_first:
                query += " AND "

            query += f'{matcher["field"]} {matcher["op"]} :{i}'  # nosec
            is_first = False
            i += 1

        if order_by:
            query += " ORDER BY "

            for field, kind in order_by.items():
                query += f" {field} {kind},"

            query = query.rstrip(",")

        query = text(query)

        with self.__client.connect() as con:
            try:
                results = con.execute(query, params).all()
            except Exception as e:
                raise e
            else:
                if not results:
                    raise ValueError("NotFound")

                if expect_one and len(results) > 1:
                    raise ValueError("Too mucth match")

                if expect_one:
                    return results[0]._asdict()

                return [result._asdict() for result in results]

            finally:
                con.close()
