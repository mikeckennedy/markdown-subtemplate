import os

import pytest

from markdown_subtemplate import engine, caching
from markdown_subtemplate import exceptions

template_folder = os.path.join(os.path.dirname(__file__), 'templates')


def test_init_folder_required():
    engine.clear_template_folder()

    with pytest.raises(exceptions.InvalidOperationException):
        engine.get_page('abc', {})


def test_init_folder_missing():
    with pytest.raises(exceptions.PathException):
        engine.set_template_folder('bad/cats/')


def test_init_folder_success():
    engine.set_template_folder(template_folder)


def test_clear_cache():
    caching.get_cache().clear()
