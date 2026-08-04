"""
speaklater
~~~~~~~~~~

Copied over from Flask-Babel which copied it from 'speaklater'
and included some fixes.
See:
  - https://github.com/python-babel/flask-babel/blob/master/flask_babel/speaklater.py
  - https://github.com/mitsuhiko/speaklater/blob/master/speaklater.py

:copyright: (c) 2010 by Armin Ronacher.
:license: BSD, see LICENSE for more details.
"""

from collections.abc import Callable, Iterator
from typing import Any, SupportsIndex, override


class LazyString:
    """A string that is only evaluated when it is actually used.

    Instances quack like :class:`str`: any attribute that is not defined
    here is looked up on the resolved string, so ``LazyString.upper()``
    and friends work as expected.
    """

    def __init__(
        self,
        func: Callable[..., str],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._func: Callable[..., str] = func
        self._args: tuple[Any, ...] = args
        self._kwargs: dict[str, Any] = kwargs

    def __getattr__(self, attr: str) -> Any:
        if attr == "__setstate__":
            raise AttributeError(attr)
        string = str(self)
        if hasattr(string, attr):
            return getattr(string, attr)
        raise AttributeError(attr)

    @override
    def __repr__(self) -> str:
        return f"l'{self!s}'"

    @override
    def __str__(self) -> str:
        return str(self._func(*self._args, **self._kwargs))

    def __len__(self) -> int:
        return len(str(self))

    def __getitem__(self, key: SupportsIndex | slice) -> str:
        return str(self)[key]

    def __iter__(self) -> Iterator[str]:
        return iter(str(self))

    def __contains__(self, item: str) -> bool:
        return item in str(self)

    def __add__(self, other: str) -> str:
        return str(self) + other

    def __radd__(self, other: str) -> str:
        return other + str(self)

    def __mul__(self, other: SupportsIndex) -> str:
        return str(self) * other

    def __rmul__(self, other: SupportsIndex) -> str:
        return other * str(self)

    def __lt__(self, other: str) -> bool:
        return str(self) < other

    def __le__(self, other: str) -> bool:
        return str(self) <= other

    @override
    def __eq__(self, other: object) -> bool:
        return str(self) == other

    @override
    def __ne__(self, other: object) -> bool:
        return str(self) != other

    def __gt__(self, other: str) -> bool:
        return str(self) > other

    def __ge__(self, other: str) -> bool:
        return str(self) >= other

    def __html__(self) -> str:
        return str(self)

    @override
    def __hash__(self) -> int:
        return hash(str(self))

    def __mod__(self, other: object) -> str:
        return str(self) % other

    def __rmod__(self, other: str) -> str:
        return other + str(self)
