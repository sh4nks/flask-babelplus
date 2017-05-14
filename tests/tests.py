# -*- coding: utf-8 -*-
from __future__ import with_statement
import unittest
from decimal import Decimal
import flask
from datetime import datetime, timedelta
import flask_babelplus as babel
from flask_babelplus import gettext, ngettext, lazy_gettext
from flask_babelplus._compat import text_type


class DateFormattingTestCase(unittest.TestCase):

    def test_basics(self):
        app = flask.Flask(__name__)
        babel.Babel(app)
        d = datetime(2010, 4, 12, 13, 46)
        delta = timedelta(days=6)

        with app.test_request_context():
            assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
            assert babel.format_date(d) == 'Apr 12, 2010'
            assert babel.format_time(d) == '1:46:00 PM'
            assert babel.format_timedelta(delta) == '1 week'
            assert babel.format_timedelta(delta, threshold=1) == '6 days'

        with app.test_request_context():
            app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
            assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'
            assert babel.format_date(d) == 'Apr 12, 2010'
            assert babel.format_time(d) == '3:46:00 PM'

        with app.test_request_context():
            app.config['BABEL_DEFAULT_LOCALE'] = 'de_DE'
            assert babel.format_datetime(d, 'long') == \
                '12. April 2010 um 15:46:00 MESZ'

    def test_init_app(self):
        b = babel.Babel()
        app = flask.Flask(__name__)
        b.init_app(app)
        d = datetime(2010, 4, 12, 13, 46)

        with app.test_request_context():
            assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
            assert babel.format_date(d) == 'Apr 12, 2010'
            assert babel.format_time(d) == '1:46:00 PM'

        with app.test_request_context():
            app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
            assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'
            assert babel.format_date(d) == 'Apr 12, 2010'
            assert babel.format_time(d) == '3:46:00 PM'

        with app.test_request_context():
            app.config['BABEL_DEFAULT_LOCALE'] = 'de_DE'
            assert babel.format_datetime(d, 'long') == \
                '12. April 2010 um 15:46:00 MESZ'

    def test_custom_formats(self):
        app = flask.Flask(__name__)
        app.config.update(
            BABEL_DEFAULT_LOCALE='en_US',
            BABEL_DEFAULT_TIMEZONE='Pacific/Johnston'
        )
        b = babel.Babel(app)
        b.date_formats['datetime'] = 'long'
        b.date_formats['datetime.long'] = 'MMMM d, yyyy h:mm:ss a'
        d = datetime(2010, 4, 12, 13, 46)

        with app.test_request_context():
            assert babel.format_datetime(d) == 'April 12, 2010 3:46:00 AM'

    def test_custom_locale_selector(self):
        app = flask.Flask(__name__)
        b = babel.Babel(app)
        d = datetime(2010, 4, 12, 13, 46)

        the_timezone = 'UTC'
        the_locale = 'en_US'

        @b.localeselector
        def select_locale():
            return the_locale

        @b.timezoneselector
        def select_timezone():
            return the_timezone

        with app.test_request_context():
            assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'

        the_locale = 'de_DE'
        the_timezone = 'Europe/Vienna'

        with app.test_request_context():
            assert babel.format_datetime(d) == '12.04.2010, 15:46:00'

    def test_refreshing(self):
        app = flask.Flask(__name__)
        babel.Babel(app)
        d = datetime(2010, 4, 12, 13, 46)
        with app.test_request_context():
            assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
            app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
            babel.refresh()
            assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'

    def test_force_locale(self):
        app = flask.Flask(__name__)
        b = babel.Babel(app)

        @b.localeselector
        def select_locale():
            return 'de_DE'

        with app.test_request_context():
            assert str(babel.get_locale()) == 'de_DE'
            with babel.force_locale('en_US'):
                assert str(babel.get_locale()) == 'en_US'
            assert str(babel.get_locale()) == 'de_DE'


class NumberFormattingTestCase(unittest.TestCase):

    def test_basics(self):
        app = flask.Flask(__name__)
        babel.Babel(app)
        n = 1099

        with app.test_request_context():
            assert babel.format_number(n) == u'1,099'
            assert babel.format_decimal(Decimal('1010.99')) == u'1,010.99'
            assert babel.format_currency(n, 'USD') == '$1,099.00'
            assert babel.format_percent(0.19) == '19%'
            assert babel.format_scientific(10000) == u'1E4'


class GettextTestCase(unittest.TestCase):

    def test_basics(self):
        app = flask.Flask(__name__)
        babel.Babel(app, default_locale='de_DE')

        with app.test_request_context():
            assert gettext(u'Hello %(name)s!', name='Peter') == 'Hallo Peter!'
            assert ngettext(u'%(num)s Apple', u'%(num)s Apples', 3) == u'3 Äpfel'  # noqa
            assert ngettext(u'%(num)s Apple', u'%(num)s Apples', 1) == u'1 Apfel'  # noqa

    def test_template_basics(self):
        app = flask.Flask(__name__)
        babel.Babel(app, default_locale='de_DE')

        def t(x):
            return flask.render_template_string('{{ %s }}' % x)

        with app.test_request_context():
            assert t("gettext('Hello %(name)s!', name='Peter')") == 'Hallo Peter!'  # noqa
            assert t("ngettext('%(num)s Apple', '%(num)s Apples', 3)") == u'3 Äpfel'  # noqa
            assert t("ngettext('%(num)s Apple', '%(num)s Apples', 1)") == u'1 Apfel'  # noqa
            assert flask.render_template_string('''
                {% trans %}Hello {{ name }}!{% endtrans %}
            ''', name='Peter').strip() == 'Hallo Peter!'
            assert flask.render_template_string('''
                {% trans num=3 %}{{ num }} Apple
                {%- pluralize %}{{ num }} Apples{% endtrans %}
            ''', name='Peter').strip() == u'3 Äpfel'

    def test_lazy_gettext(self):
        app = flask.Flask(__name__)
        babel.Babel(app, default_locale='de_DE')
        yes = lazy_gettext(u'Yes')
        with app.test_request_context():
            assert text_type(yes) == 'Ja'
        app.config['BABEL_DEFAULT_LOCALE'] = 'en_US'
        with app.test_request_context():
            assert text_type(yes) == 'Yes'

    def test_no_formatting(self):
        """
        Ensure we don't format strings unless a variable is passed.
        """
        app = flask.Flask(__name__)
        babel.Babel(app)

        with app.test_request_context():
            assert gettext(u'Test %s') == u'Test %s'
            assert gettext(u'Test %(name)s', name=u'test') == u'Test test'
            assert gettext(u'Test %s') % 'test' == u'Test test'

    def test_lazy_gettext_defaultdomain(self):
        app = flask.Flask(__name__)
        domain = babel.Domain(domain='test')
        babel.Babel(app, default_locale='de_DE', default_domain=domain)
        first = lazy_gettext('first')
        with app.test_request_context():
            assert text_type(first) == 'erste'
        app.config['BABEL_DEFAULT_LOCALE'] = 'en_US'
        with app.test_request_context():
            assert text_type(first) == 'first'

    def test_list_translations(self):
        app = flask.Flask(__name__)
        b = babel.Babel(app, default_locale='de_DE')

        # an app_context is automatically created when a request context
        # is pushed if necessary
        with app.test_request_context():
            translations = b.list_translations()
            assert len(translations) == 1
            assert str(translations[0]) == 'de'

    def test_domain(self):
        app = flask.Flask(__name__)
        babel.Babel(app, default_locale='de_DE')
        domain = babel.Domain(domain='test')

        with app.test_request_context():
            assert domain.gettext('first') == 'erste'
            assert babel.gettext('first') == 'first'

    def test_as_default(self):
        app = flask.Flask(__name__)
        babel.Babel(app, default_locale='de_DE')
        domain = babel.Domain(domain='test')

        with app.test_request_context():
            assert babel.gettext('first') == 'first'
            domain.as_default()
            assert babel.gettext('first') == 'erste'

    def test_default_domain(self):
        app = flask.Flask(__name__)
        domain = babel.Domain(domain='test')
        babel.Babel(app, default_locale='de_DE', default_domain=domain)

        with app.test_request_context():
            assert babel.gettext('first') == 'erste'

    def test_multiple_apps(self):
        app1 = flask.Flask(__name__)
        babel.Babel(app1, default_locale='de_DE')

        app2 = flask.Flask(__name__)
        babel.Babel(app2, default_locale='de_DE')

        with app1.test_request_context():
            assert babel.gettext('Yes') == 'Ja'
            assert 'de_DE' in app1.extensions["babel"].domain.cache

        with app2.test_request_context():
            assert 'de_DE' not in app2.extensions["babel"].domain.cache


if __name__ == '__main__':
    unittest.main()
