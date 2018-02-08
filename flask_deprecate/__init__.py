"""
A tool for deprecating APIs in Flask.
Injects a head for clients to catch and
indicates the upgrade path.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask_deprecate.flask_deprecate import deprecate_blueprint, deprecate_route

__all__ = ['deprecate_blueprint', 'deprecate_route']
__author__ = 'Tim Martin'
__email__ = 'oss@timmartin.me'
__version__ = '0.1.3'
