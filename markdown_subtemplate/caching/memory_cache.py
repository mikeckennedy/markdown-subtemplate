from datetime import datetime

from .cache_entry import CacheEntry
from .subtemplate_cache import SubtemplateCache


class MemoryCache(SubtemplateCache):
    markdown_cache = {}
    html_cache = {}

    def get_html(self, key: str) -> CacheEntry:
        return self.html_cache.get(key)

    def add_html(self, key: str, name: str, html_contents: str) -> CacheEntry:
        entry = CacheEntry(key=key, name=name, created=datetime.now(), contents=html_contents)
        self.html_cache[key] = entry

        return entry

    def get_markdown(self, key: str) -> CacheEntry:
        return self.markdown_cache.get(key)

    def add_markdown(self, key: str, name: str, markdown_contents: str) -> CacheEntry:
        entry = CacheEntry(key=key, name=name, created=datetime.now(), contents=markdown_contents)
        self.markdown_cache[key] = entry

        return entry

    def clear(self):
        self.markdown_cache.clear()
        self.html_cache.clear()

    def count(self) -> int:
        return len(self.markdown_cache) + len(self.html_cache)
