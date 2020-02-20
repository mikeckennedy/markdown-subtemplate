from .cache_entry import CacheEntry
from .memory_cache import MemoryCache
from .subtemplate_cache import SubtemplateCache
from ..exceptions import ArgumentExpectedException

cache: SubtemplateCache = MemoryCache()


def set_cache(cache_instance: SubtemplateCache):
    global cache
    if not cache_instance or not isinstance(cache_instance, SubtemplateCache):
        raise ArgumentExpectedException('cache_instance')

    cache = cache_instance
