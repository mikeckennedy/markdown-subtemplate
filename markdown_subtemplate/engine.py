import os
from typing import Optional, Any, Dict

from .infrastructure import page as __page
from . import logging as __logging
from . import caching as __caching

__template_folder: Optional[str] = None


def set_template_folder(full_path: str):
    from .exceptions import PathException
    log = __logging.get_log()

    global __template_folder

    test_path = os.path.abspath(full_path)
    if test_path != full_path:
        msg = f"{full_path} is not an absolute path."
        log.error("engine.set_template_folder: " + msg)
        raise PathException(msg)

    if not os.path.exists(full_path):
        msg = f"{full_path} does not exist."
        log.error("engine.set_template_folder: " + msg)
        raise PathException(msg)

    if not os.path.isdir(full_path):
        msg = f"{full_path} is not a directory."
        log.error("engine.set_template_folder: " + msg)
        raise PathException(msg)

    log.info(f"Template folder set: {full_path}")

    __template_folder = full_path
    __page.template_folder = full_path


def get_page(template_path: str, data: Dict[str, Any] = {}) -> str:
    from markdown_subtemplate.exceptions import InvalidOperationException
    log = __logging.get_log()

    if not __template_folder:
        msg = "Template folder not set, call engine.set_template_folder() first."
        log.error("engine.get_page: " + msg)
        raise InvalidOperationException(msg)

    log.verbose(f"engine.get_page: Getting page content for {template_path}")
    return __page.get_page(template_path, data)


def clear_cache():
    log = __logging.get_log()
    cache = __caching.get_cache()

    item_count = cache.count()
    cache.clear()

    log.info(f"engine.clear_cache: Cache cleared, reclaimed {item_count:,} items.")


def clear_template_folder():
    global __template_folder
    __template_folder = None
