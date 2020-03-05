from typing import Any, Dict

from . import caching as __caching, storage
from . import logging as __logging
from .infrastructure import page as __page


def get_page(template_path: str, data: Dict[str, Any] = {}) -> str:
    from markdown_subtemplate.exceptions import InvalidOperationException
    log = __logging.get_log()

    if not storage.is_initialized():
        msg = "Storage engine is not initialized."
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

