"""
Business logic.  Kept separate in case the project
becomes larger for some reason in the future.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import logging

from flask import request

_LOG = logging.getLogger(__name__)
_BLUEPRINT_PREFIXES = {}


def deprecate_blueprint(old_blueprint, new_blueprint=None, message=''):
    """
    Deprecates an every route on a blueprint by adding a
    header "WARNING" with a message.

    If a url_prefix is set for the blueprint in either
    the blueprint init or the registration with the app,
    then an additional section on the header will appear
    saying the blueprint is deprecated. If a new_blueprint
    is also provided, the header will have additional
    info directing the client to the new URL.  Note, that
    this will not automatically redirect the client.

    The blueprint must be deprecated before registering it
    with the application

    >>> from flask import Flask, Blueprint
    >>> app = Flask('myapp')
    >>> deprecated_bp = Blueprint('deprecated', 'deprecated')
    >>> new_bp = Blueprint('new', 'new')
    >>> deprecate_blueprint(old_blueprint, new_blueprint=new_bp)
    >>> app.register_blueprint(bp, url_prefix='/v1')
    >>> app.register_blueprint(new_bp, url_prefix='/v2')


    :param flask.Blueprint old_blueprint: The blueprint to be deprecated
    :param flask.Blueprint new_blueprint: The new blueprint that will be
        replacing the old one (if applicable).
    :param str message: An extra message to append
        to the warning header
    :rtype: NoneType
    """
    _setup_url_prefix(old_blueprint)
    if new_blueprint:
        _setup_url_prefix(new_blueprint)

    def _after_request_handler(response):
        full_message = _build_blueprint_message(request, old_blueprint, new_blueprint, message)
        return _warn_deprecated_view(response, full_message)
    old_blueprint.after_request(_after_request_handler)


def deprecate_route(message=''):
    """
    Adds a Warning header to the response
    informing the client that the route is deprecated

    .. code-block:: python

        from flask import Flask, Response
        from flask_deprecate import deprecate_route

        app = Flask('myapp')

        @app.route('/my_route')
        @deprecate_route()
        def deprecated_route():
            return Response()

    :param str message: Additional information to provide
        to the client
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            return _warn_deprecated_view(resp, message)
        return _wrapper
    return _decorator


def _warn_deprecated_view(response, message, log_level=logging.WARNING):
    response.headers['Warning'] = message
    _LOG.log(log_level, message)
    return response


def _on_blueprint_register(state):
    _BLUEPRINT_PREFIXES[state.blueprint] = state.url_prefix


def _setup_url_prefix(blueprint):
    blueprint.record_once(_on_blueprint_register)


def _build_base_message(message=''):
    full_message = '{0} is deprecated;{1}'.format(request.base_url, message)
    return '299 - "Deprecated API : {0}"'.format(full_message)


def _build_base_blueprint_message(root_url, message=''):
    blueprint_message = '{0} is deprecated;{1}'.format(root_url, message)
    return _build_base_message(message=blueprint_message)


def _build_new_blueprint_message(old_root_url, new_root_url, message=''):
    new_url_message = 'Use {0} instead;{1}'.format(new_root_url, message)
    return _build_base_blueprint_message(old_root_url, new_url_message)


def _build_blueprint_message(req, old_blueprint, new_blueprint, message):
    if _BLUEPRINT_PREFIXES[old_blueprint] is None:
        return _build_base_message(message)
    old_blueprint_url = _join_url(req.url_root, _BLUEPRINT_PREFIXES[old_blueprint])
    if new_blueprint and _BLUEPRINT_PREFIXES[new_blueprint] is not None:
        new_blueprint_url = _join_url(req.url_root, _BLUEPRINT_PREFIXES[new_blueprint])
        return _build_new_blueprint_message(old_blueprint_url, new_blueprint_url, message)
    return _build_base_blueprint_message(old_blueprint_url, message)


def _join_url(root, prefix):
    return '/'.join([root.rstrip('/'), prefix.lstrip('/')])
