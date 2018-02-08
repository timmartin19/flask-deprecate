import unittest
from mock import Mock

from flask_deprecate.flask_deprecate import _build_blueprint_message, _build_base_blueprint_message, \
    _build_base_message, _build_new_blueprint_message, _join_url, _warn_deprecated_view, deprecate_blueprint, \
    _BLUEPRINT_PREFIXES, deprecate_route
from flask import Flask, Blueprint, Response
from webtest import TestApp


class TestBuildMessages(unittest.TestCase):
    def setUp(self):
        self.app = Flask('blah')
        self.app_context = self.app.test_request_context('/api')
        self.app_context.push()
        _BLUEPRINT_PREFIXES.clear()

    def tearDown(self):
        self.app_context.pop()

    def test_build_base_message__when_no_message(self):
        resp = _build_base_message()
        self.assertEquals('299 - "Deprecated API : http://localhost/api is deprecated;"', resp)

    def test_build_base_message__when_message(self):
        message = "some message"
        resp = _build_base_message(message)
        self.assertTrue(resp.endswith('{}"'.format(message)))

    def test_build_base_blueprint_message(self):
        message = "blah"
        resp = _build_base_blueprint_message('/some_root', message=message)
        resp_parts = resp.strip('"').strip(';').split(';')
        self.assertEqual(len(resp_parts), 3)
        self.assertIn('/some_root is deprecated', resp_parts)

    def test_build_new_blueprint_message(self):
        message = 'blah'
        resp = _build_new_blueprint_message('/old', '/new', message)
        resp_parts = resp.strip('"').strip(';').split(';')
        self.assertEqual(len(resp_parts), 4)
        self.assertIn('Use /new instead', resp_parts)

    def test_build_blueprint_message__when_no_new_blueprint(self):
        old_blueprint = Mock(url_prefix='/old')
        _BLUEPRINT_PREFIXES[old_blueprint] = '/old'
        req = Mock(url_root='/api')
        resp = _build_blueprint_message(req, old_blueprint, None, 'blah')
        resp_parts = resp.strip('"').strip(';').split(';')
        self.assertEqual(len(resp_parts), 3)

    def test_build_blueprint_message__when_new_blueprint(self):
        old_blueprint = Mock(url_prefix='/old')
        req = Mock(url_root='/api')
        new_bp = Mock(url_prefix='/new')
        _BLUEPRINT_PREFIXES[old_blueprint] = '/old'
        _BLUEPRINT_PREFIXES[new_bp] = '/new'
        resp = _build_blueprint_message(req, old_blueprint, new_bp, 'blah')
        resp_parts = resp.strip('"').strip(';').split(';')
        self.assertEqual(len(resp_parts), 4)

    def test_build_blueprint_message__when_no_prefix(self):
        old_blueprint = Mock(url_prefix='/old')
        req = Mock(url_root='/api')
        _BLUEPRINT_PREFIXES[old_blueprint] = None
        resp = _build_blueprint_message(req, old_blueprint, None, 'blah')
        resp_parts = resp.strip('"').strip(';').split(';')
        self.assertEqual(len(resp_parts), 2)


class TestJoinUrl(unittest.TestCase):
    def test_when_root_suffix_slash(self):
        resp = _join_url('/root/', 'suffix/')
        self.assertEqual('/root/suffix/', resp)

    def test_when_prefix_prefix_slash(self):
        resp = _join_url('/root', '/suffix/')
        self.assertEqual('/root/suffix/', resp)

    def test_when_no_extra_slashes(self):
        resp = _join_url('/root', 'suffix/')
        self.assertEqual('/root/suffix/', resp)


class TestWarnDeprecatedView(unittest.TestCase):
    def test_warn_deprecated_view(self):
        response = Mock(headers={})
        resp = _warn_deprecated_view(response, 'some message')
        self.assertEqual(resp.headers['Warning'], 'some message')


class TestDeprecateBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask('blah')
        self.test_app = TestApp(self.app)
        _BLUEPRINT_PREFIXES.clear()

    def test_when_no_url_prefix(self):
        bp = Blueprint('old', 'old')

        @bp.route('/some')
        def blah():
            return Response()

        deprecate_blueprint(bp)
        self.app.register_blueprint(bp)

        resp = self.test_app.get('/some')
        self.assertIn('Warning', resp.headers)

    def test_when_url_prefix_on_register(self):
        bp = Blueprint('old', 'old', url_prefix='/blah')

        @bp.route('/some')
        def blah():
            return Response()

        deprecate_blueprint(bp)
        self.app.register_blueprint(bp)

        resp = self.test_app.get('/blah/some')
        self.assertIn('Warning', resp.headers)

    def test_when_url_prefix_on_init(self):
        bp = Blueprint('old', 'old')
        new_bp = Blueprint('new', 'new')

        @bp.route('/some')
        @new_bp.route('/some')
        def blah():
            return Response()

        deprecate_blueprint(bp, new_bp)
        self.app.register_blueprint(bp, url_prefix='/blah')
        self.app.register_blueprint(new_bp, url_prefix='/new')

        resp = self.test_app.get('/blah/some')
        self.assertIn('Warning', resp.headers)


class TestDeprecatedView(unittest.TestCase):
    def setUp(self):
        self.app = Flask('blah')
        self.test_app = TestApp(self.app)

    def test_when_after_route_decorator(self):
        @self.app.route('/blah')
        @deprecate_route()
        def blah():
            return Response()

        resp = self.test_app.get('/blah')
        self.assertIn('Warning', resp.headers)
