from api.api import API
from api.fetcher import Fetcher
from db.db import DB
import sqlalchemy as sa
from typing import TypeVar, Generic, Callable

T = TypeVar('T')

class Builder(Generic[T]):
    def __init__(self, fnc: Callable[[], T]) -> None:
        self.cached_object: T | None = None
        self.fetcher: Callable[[], T] = fnc

    def build(self):
        if self.cached_object is None:
            self.cached_object = self.fetcher()
        return self.cached_object

class EngineBuilder(Builder[sa.Engine]):
    def __init__(self) -> None:
        super().__init__(self.get_engine)

    def get_engine(self) -> sa.Engine:
        return sa.create_engine('sqlite:///../data/NYTListings.db')

class DBBuilder(Builder[DB]):
    def __init__(self) -> None:
        super().__init__(self.get_db)

    def get_db(self) -> DB:
        return DB(engine_builder.build())

class FetcherBuilder(Builder[Fetcher]):
    def __init__(self) -> None:
        super().__init__(self.get_fetcher)

    def get_fetcher(self) -> Fetcher:
        return Fetcher(db_builder.build())

class APIBuilder(Builder[API]):
    def __init__(self) -> None:
        super().__init__(self.get_api)

    def get_api(self) -> API:
        return API(fetcher_builder.build())

engine_builder: EngineBuilder = EngineBuilder()
db_builder: DBBuilder = DBBuilder()
fetcher_builder: FetcherBuilder = FetcherBuilder()
api_builder: APIBuilder = APIBuilder()
