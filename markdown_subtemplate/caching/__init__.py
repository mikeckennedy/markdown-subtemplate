from .cache_entry import CacheEntry
from .memory_cache import MemoryCache
from .subtemplate_cache import SubtemplateCache
from ..exceptions import ArgumentExpectedException

__cache: SubtemplateCache = MemoryCache()


def set_cache(cache_instance: SubtemplateCache):
    global __cache
    if not cache_instance or not isinstance(cache_instance, SubtemplateCache):
        raise ArgumentExpectedException('cache_instance')

    __cache = cache_instance


def get_cache() -> SubtemplateCache:
    return __cache
