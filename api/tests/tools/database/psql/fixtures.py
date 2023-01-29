from glob import escape, glob
from typing import final

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from tests.config import DB_CONNECTION_STRING
from tests.tools import database


class Fixtures(database.Fixtures):
    __client: Engine = None  # type: ignore

    def __init__(self) -> None:
        if not Fixtures.__client:
            Fixtures.__client = create_engine(
                DB_CONNECTION_STRING,
                future=True,
                echo=True,
                pool_size=50,
                max_overflow=50,
                pool_pre_ping=True,
                pool_recycle=8 * 60,  # seconds
            )
        self.__base_path: str = ""
        self.__with_folder: str = ""

    def __path__(self) -> str:
        return escape(f"{self.__base_path}{self.__with_folder}")

    def with_base_path(self, path: str) -> database.Fixtures:
        self.__base_path = (path + "/").replace("//", "/")

        return self

    def with_folder(self, path: str) -> database.Fixtures:
        self.__with_folder = (path.lstrip("/") + "/").replace("//", "/")

        return self

    def load_scripts(self) -> None:
        files = glob(self.__path__() + "*.sql")
        files.sort()

        for file in files:
            self.load_script(file)

    def load_script(self, name: str) -> database.Fixtures:
        path = self.__path__()
        if not name.startswith(path):
            name = path + name

        with self.__client.connect() as con:
            with open(name) as src:
                try:
                    query = text(src.read())
                    con.execute(query)
                    con.commit()
                except IntegrityError as e:
                    con.rollback()
                    print(e)
                except Exception as e:
                    con.rollback()
                    raise e
                finally:
                    con.close()

        return self
