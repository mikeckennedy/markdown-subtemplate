import os
from typing import Optional, Any, Dict

from . import page as __page

__template_folder: Optional[str] = None


def set_template_folder(full_path: str):
    from .exceptions import PathException
    global __template_folder

    test_path = os.path.abspath(full_path)
    if test_path != full_path:
        raise PathException(f"{full_path} is not an absolute path.")

    if not os.path.exists(full_path):
        raise PathException(f"{full_path} does not exist.")

    if not os.path.isdir(full_path):
        raise PathException(f"{full_path} is not a directory.")

    __template_folder = full_path
    __page.template_folder = full_path


def get_page(template_path: str, data: Dict[str, Any] = {}) -> str:
    from markdown_subtemplate._impl.exceptions import InvalidOperationException

    if not __template_folder:
        raise InvalidOperationException("Template folder not set, call engine.set_template_folder() first.")

    return __page.get_page(template_path, data)


def clear_cache(reclaim_all_memory=False):
    __page.clear_cache(reclaim_all_memory)


def clear_template_folder():
    global __template_folder
    __template_folder = None
