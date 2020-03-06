import abc
from typing import Optional

from .cache_entry import CacheEntry


class SubtemplateCache(abc.ABC):
    @abc.abstractmethod
    def get_html(self, key: str) -> CacheEntry:
        pass

    @abc.abstractmethod
    def add_html(self, key: str, name: str, html_contents: str) -> CacheEntry:
        pass

    @abc.abstractmethod
    def get_markdown(self, key: str) -> CacheEntry:
        pass

    @abc.abstractmethod
    def add_markdown(self, key: str, name: str, markdown_contents: str) -> CacheEntry:
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def count(self) -> int:
        pass


