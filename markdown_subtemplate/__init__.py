"""
markdown_subtemplate - A template engine to render
Markdown with external template imports and variable replacements.
"""

__version__ = '0.1.2'
__author__ = 'Michael Kennedy <michael@talkpython.fm>'
__all__ = []

from ._impl import engine
from ._impl import exceptions
from ._impl import logging
# from ._impl import markdown_transformer
# from ._impl import page
