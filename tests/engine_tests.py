import os

import pytest

from markdown_subtemplate import engine, caching, storage
from markdown_subtemplate import exceptions

template_folder = os.path.join(os.path.dirname(__file__), 'templates')


def test_init_folder_required():
    storage.get_storage().clear_settings()

    with pytest.raises(exceptions.InvalidOperationException):
        engine.get_page('abc', {})


def test_init_folder_missing():
    with pytest.raises(exceptions.PathException):
        storage.file_storage.FileStore.set_template_folder('bad/cats/')


def test_init_folder_success():
    storage.file_storage.FileStore.set_template_folder(template_folder)


def test_clear_cache():
    caching.get_cache().clear()
