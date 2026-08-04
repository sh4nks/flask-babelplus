"""
flask_babelplus
~~~~~~~~~~~~~~~

Implements i18n/l10n support for Flask applications based on Babel.

:copyright: (c) 2013 by Serge S. Koval, Armin Ronacher and contributors.
:license: BSD, see LICENSE for more details.
"""

from importlib.metadata import version

from .constants import DateFormat, DateFormatKey, DateFormatWidth
from .core import Babel
from .domain import (
    Domain,
    get_domain,
    gettext,
    lazy_gettext,
    lazy_ngettext,
    lazy_pgettext,
    ngettext,
    npgettext,
    pgettext,
)
from .speaklater import LazyString
from .utils import (
    Number,
    TimedeltaGranularity,
    force_locale,
    format_currency,
    format_date,
    format_datetime,
    format_decimal,
    format_number,
    format_percent,
    format_scientific,
    format_time,
    format_timedelta,
    get_locale,
    get_timezone,
    refresh,
    to_user_timezone,
    to_utc,
)

__version__: str = version("Flask-BabelPlus")
__all__ = (
    "Babel",
    "DateFormat",
    "DateFormatKey",
    "DateFormatWidth",
    "Domain",
    "LazyString",
    "Number",
    "TimedeltaGranularity",
    "force_locale",
    "format_currency",
    "format_date",
    "format_datetime",
    "format_decimal",
    "format_number",
    "format_percent",
    "format_scientific",
    "format_time",
    "format_timedelta",
    "get_domain",
    "get_locale",
    "get_timezone",
    "gettext",
    "lazy_gettext",
    "lazy_ngettext",
    "lazy_pgettext",
    "ngettext",
    "npgettext",
    "pgettext",
    "refresh",
    "to_user_timezone",
    "to_utc",
)
