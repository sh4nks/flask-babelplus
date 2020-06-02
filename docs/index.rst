Flask-BabelPlus
===============

.. module:: flask_babelplus

Flask-BabelPlus is an extension to `Flask`_ that adds i18n and l10n support to
any Flask application with the help of `babel`_, `pytz`_ and
`speaklater`_.  It has builtin support for date formatting with timezone
support as well as a very simple and friendly interface to :mod:`gettext`
translations.


Installation
------------

Install the extension with one of the following commands::

    $ easy_install Flask-BabelPlus

or alternatively if you have pip installed::

    $ pip install Flask-BabelPlus

Please note that Flask-BabelPlus requires Jinja 2.5.  If you are using an
older version you will have to upgrade or disable the Jinja support.


Configuration
-------------

To get started all you need to do is to instanciate a :class:`Babel`
object after configuring the application::

    from flask import Flask
    from flask_babelplus import Babel

    app = Flask(__name__)
    app.config.from_pyfile('mysettings.cfg')
    babel = Babel(app)

The main difference from `Flask-BabelEx`_ is, that you can configure
Flask-BabelPlus when using the factory method of initializing extensions::

    # Flask-BabelPlus
    babel.init_app(app=app, default_domain=FlaskBBDomain(app))

The babel object itself can be used to configure the babel support
further.  Babel has two configuration values that can be used to change
some internal defaults:

=========================== =============================================
`BABEL_DEFAULT_LOCALE`      The default locale to use if no locale
                            selector is registered.  This defaults
                            to ``'en'``.
`BABEL_DEFAULT_TIMEZONE`    The timezone to use for user facing dates.
                            This defaults to ``'UTC'`` which also is the
                            timezone your application must use internally.
=========================== =============================================

For more complex applications you might want to have multiple applications
for different users which is where selector functions come in handy.  The
first time the babel extension needs the locale (language code) of the
current user it will call a :meth:`~Babel.localeselector` function, and
the first time the timezone is needed it will call a
:meth:`~Babel.timezoneselector` function.

If any of these methods return `None` the extension will automatically
fall back to what's in the config.  Furthermore for efficiency that
function is called only once and the return value then cached.  If you
need to switch the language between a request, you can :func:`refresh` the
cache.

Example selector functions::

    from flask import g, request

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.
        return request.accept_languages.best_match(['de', 'fr', 'en'])

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone

The example above assumes that the current user is stored on the
:data:`flask.g` object.

Formatting Dates
----------------

To format dates you can use the :func:`format_datetime`,
:func:`format_date`, :func:`format_time` and :func:`format_timedelta`
functions.  They all accept a :class:`datetime.datetime` (or
:class:`datetime.date`, :class:`datetime.time` and
:class:`datetime.timedelta`) object as first parameter and then optionally
a format string.  The application should use naive datetime objects
internally that use UTC as timezone.  On formatting it will automatically
convert into the user's timezone in case it differs from UTC.

To play with the date formatting from the console, you can use the
:meth:`~flask.Flask.test_request_context` method:

>>> app.test_request_context().push()

Here some examples:

>>> from flask_babelplus import format_datetime
>>> from datetime import datetime
>>> format_datetime(datetime(1987, 3, 5, 17, 12))
u'Mar 5, 1987 5:12:00 PM'
>>> format_datetime(datetime(1987, 3, 5, 17, 12), 'full')
u'Thursday, March 5, 1987 5:12:00 PM World (GMT) Time'
>>> format_datetime(datetime(1987, 3, 5, 17, 12), 'short')
u'3/5/87 5:12 PM'
>>> format_datetime(datetime(1987, 3, 5, 17, 12), 'dd mm yyy')
u'05 12 1987'
>>> format_datetime(datetime(1987, 3, 5, 17, 12), 'dd mm yyyy')
u'05 12 1987'

And again with a different language:

>>> app.config['BABEL_DEFAULT_LOCALE'] = 'de'
>>> from flask_babelplus import refresh; refresh()
>>> format_datetime(datetime(1987, 3, 5, 17, 12), 'EEEE, d. MMMM yyyy H:mm')
u'Donnerstag, 5. M\xe4rz 1987 17:12'

For more format examples head over to the `babel`_ documentation.

Using Translations
------------------

The other big part next to date formatting are translations.  For that,
Flask uses :mod:`gettext` together with Babel.  The idea of gettext is
that you can mark certain strings as translatable and a tool will pick all
those up, collect them in a separate file for you to translate.  At
runtime the original strings (which should be English) will be replaced by
the language you selected.

There are two functions responsible for translating: :func:`gettext` and
:func:`ngettext`.  The first to translate singular strings and the second
to translate strings that might become plural.  Here some examples::

    from flask_babelplus import gettext, ngettext

    gettext(u'A simple string')
    gettext(u'Value: %(value)s', value=42)
    ngettext(u'%(num)s Apple', u'%(num)s Apples', number_of_apples)

Additionally if you want to use constant strings somewhere in your
application and define them outside of a request, you can use a lazy
strings.  Lazy strings will not be evaluated until they are actually used.
To use such a lazy string, use the :func:`lazy_gettext` function::

    from flask_babelplus import lazy_gettext

    class MyForm(formlibrary.FormBase):
        success_message = lazy_gettext(u'The form was successfully saved.')

So how does Flask-BabelPlus find the translations?  Well first you have to
create some.  Here is how you do it:

Translating Applications
````````````````````````

First you need to mark all the strings you want to translate in your
application with :func:`gettext` or :func:`ngettext`.  After that, it's
time to create a ``.pot`` file.  A ``.pot`` file contains all the strings
and is the template for a ``.po`` file which contains the translated
strings.  Babel can do all that for you.

First of all you have to get into the folder where you have your
application and create a mapping file.  For typical Flask applications, this
is what you want in there:

.. sourcecode:: ini

    [python: **.py]
    [jinja2: **/templates/**.html]
    extensions=jinja2.ext.autoescape,jinja2.ext.with_

Save it as ``babel.cfg`` or something similar next to your application.
Then it's time to run the `pybabel` command that comes with Babel to
extract your strings::

    $ pybabel extract -F babel.cfg -o messages.pot .

If you are using the :func:`lazy_gettext` function you should tell pybabel
that it should also look for such function calls::

    $ pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

This will use the mapping from the ``babel.cfg`` file and store the
generated template in ``messages.pot``.  Now we can create the first
translation.  For example to translate to German use this command::

    $ pybabel init -i messages.pot -d translations -l de

``-d translations`` tells pybabel to store the translations in this
folder.  This is where Flask-BabelPlus will look for translations.  Put it
next to your template folder.

Now edit the ``translations/de/LC_MESSAGES/messages.po`` file as needed.
Check out some gettext tutorials if you feel lost.

To compile the translations for use, ``pybabel`` helps again::

    $ pybabel compile -d translations

What if the strings change?  Create a new ``messages.pot`` like above and
then let ``pybabel`` merge the changes::

    $ pybabel update -i messages.pot -d translations

Afterwards some strings might be marked as fuzzy (where it tried to figure
out if a translation matched a changed key).  If you have fuzzy entries,
make sure to check them by hand and remove the fuzzy flag before
compiling.

Flask-BabelPlus looks for message catalogs in ``translations`` directory
which should be located under Flask application directory. Default
domain is "messages".

For example, if you want to have translations for German, Spanish and French,
directory structure should look like this:

    translations/de/LC_MESSAGES/messages.mo
    translations/sp/LC_MESSAGES/messages.mo
    translations/fr/LC_MESSAGES/messages.mo

Translation Domains
```````````````````

By default, Flask-BabelPlus will use "messages" domain, which will make it use translations
from the ``messages.mo`` file. It is not very convenient for third-party Flask extensions,
which might want to localize themselves without requiring user to merge their translations
into "messages" domain.

Flask-BabelPlus allows extension developers to specify which translation domain to
use::

    from flask_babelplus import Domain

    mydomain = Domain(domain='myext')

    mydomain.lazy_gettext('Hello World!')

:class:`Domain` contains all gettext-related methods (:meth:`~Domain.gettext`,
:meth:`~Domain.ngettext`, etc).

In previous example, localizations will be read from the ``myext.mo`` files, but
they have to be located in ``translations`` directory under users Flask application.
If extension is distributed with the localizations, it is possible to specify
their location::

    from flask_babelplus import Domain

    from flask_myext import translations
    mydomain = Domain(translations.__path__[0])

``mydomain`` will look for translations in extension directory with default (messages)
domain.

It is also possible to change the translation domain used by default,
either for each app or per request.

To set the :class:`Domain` that will be used in an app, pass it to
:class:`Babel` on initialization::

    from flask import Flask
    from flask_babelplus import Babel, Domain

    app = Flask(__name__)
    domain = Domain(domain='myext')
    babel = Babel(app, default_domain=domain)

Translations will then come from the ``myext.mo`` files by default.

To change the default domain in a request context, call the
:meth:`~Domain.as_default` method from within the request context::

    from flask import Flask
    from flask_babelplus import Babel, Domain, gettext

    app = Flask(__name__)
    domain = Domain(domain='myext')
    babel = Babel(app)

    @app.route('/path')
    def demopage():
        domain.as_default()

        return gettext('Hello World!')

``Hello World!`` will get translated using the ``myext.mo`` files, but
other requests will use the default ``messages.mo``. Note that a
:class:`Babel` must be initialized for the app for translations to
work at all.

Troubleshooting
---------------

On Snow Leopard pybabel will most likely fail with an exception.  If this
happens, check if this command outputs UTF-8::

    $ echo $LC_CTYPE
    UTF-8

This is a OS X bug unfortunately.  To fix it, put the following lines into
your ``~/.profile`` file::

    export LC_CTYPE=en_US.utf-8

Then restart your terminal.

API
---

This part of the documentation documents each and every public class or
function from Flask-BabelPlus.

Configuration
`````````````

.. autoclass:: Babel
   :members:

Context Functions
`````````````````

.. autofunction:: get_locale

.. autofunction:: get_timezone

Translation domains
```````````````````

.. autoclass:: Domain
    :members:

Datetime Functions
``````````````````

.. autofunction:: to_user_timezone

.. autofunction:: to_utc

.. autofunction:: format_datetime

.. autofunction:: format_date

.. autofunction:: format_time

.. autofunction:: format_timedelta

Gettext Functions
`````````````````

These are just shortcuts for the default Flask domain.

.. function:: gettext

Equivalent to :meth:`Domain.gettext`.

.. function:: ngettext

Equivalent to :meth:`Domain.ngettext`.

.. function:: pgettext

Equivalent to :meth:`Domain.pgettext`.

.. function:: npgettext

Equivalent to :meth:`Domain.npgettext`.

.. function:: lazy_gettext

Equivalent to :meth:`Domain.lazy_gettext`.

.. function:: lazy_ngettext

Equivalent to :meth:`Domain.lazy_ngettext`.

.. function:: lazy_pgettext

Equivalent to :meth:`Domain.lazy_pgettext`.


Low-Level API
`````````````

.. autofunction:: refresh

.. autofunction:: force_locale


Additional Information
----------------------

.. toctree::
   :maxdepth: 2

   changelog
   license

* :ref:`search`


.. _Flask: http://flask.pocoo.org/
.. _babel: http://babel.edgewall.org/
.. _pytz: http://pytz.sourceforge.net/
.. _speaklater: https://github.com/sh4nks/flask-babelplus/blob/master/flask_babelplus/speaklater.py
.. _Flask-BabelEx: https://github.com/mrjoes/flask-babelex
