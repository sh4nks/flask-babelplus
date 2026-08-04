"""
flask_babelplus.constants
~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the constants that are used in this
extension.

:copyright: (c) 2013 by Armin Ronacher, Daniel Neuhäuser and contributors.
:license: BSD, see LICENSE for more details.
"""

from typing import Literal

from werkzeug.datastructures import ImmutableDict

#: The width of a date/time format. Anything else is treated as a literal
#: Babel format pattern.
type DateFormatWidth = Literal["short", "medium", "long", "full"]

#: A date/time format: either a width, a Babel format pattern, or ``None``
#: to fall back to the locale default.
type DateFormat = DateFormatWidth | str | None

#: A key into :data:`DEFAULT_DATE_FORMATS` / :attr:`Babel.date_formats`.
type DateFormatKey = Literal[
    "time",
    "date",
    "datetime",
    "time.short",
    "time.medium",
    "time.full",
    "time.long",
    "date.short",
    "date.medium",
    "date.full",
    "date.long",
    "datetime.short",
    "datetime.medium",
    "datetime.full",
    "datetime.long",
]

DEFAULT_LOCALE: str = "en"
DEFAULT_TIMEZONE: str = "UTC"
DEFAULT_DATE_FORMATS: ImmutableDict[DateFormatKey, DateFormat] = ImmutableDict(
    {
        "time": "medium",
        "date": "medium",
        "datetime": "medium",
        "time.short": None,
        "time.medium": None,
        "time.full": None,
        "time.long": None,
        "date.short": None,
        "date.medium": None,
        "date.full": None,
        "date.long": None,
        "datetime.short": None,
        "datetime.medium": None,
        "datetime.full": None,
        "datetime.long": None,
    }
)
