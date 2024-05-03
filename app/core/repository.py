from abc import ABC, abstractmethod
from typing import Sequence, Callable, Optional


class Repository[T, S](ABC):

    @abstractmethod
    async def find(
        self, session: S, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self, session: S, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def total(self, session: S, filter_func: Optional[Callable] = None, **filters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_by_pk(self, session: S, pk: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, session: S, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, session: S, pk: int, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, session: S, pk: int) -> None:
        raise NotImplementedError
