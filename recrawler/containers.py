"""Containers module."""

from collections import UserDict
from typing import Iterable, Generator
from urllib.parse import urldefrag


def normalize_url(url: str) -> str:
    """Removes from url fragment and trailing slash

    :param url: url to normalize
    :type url: str
    :return: normalized url
    :rtype: str
    """
    return urldefrag(url).url.rstrip('/')


class LinksSet():
    def __init__(self):
        self.data = set()

    def add(self, link: str) -> bool:
        norm_url = normalize_url(link)
        if norm_url in self.data:
            return False
        self.data.add(norm_url)
        return True

    def __lshift__(self, link: str) -> bool:
        return self.add(link)

    def add_multiple(self, links: Iterable) -> int:
        return sum(self.add(link) for link in links)

    def __contains__(self: object, link: str) -> bool:
        return normalize_url(link) in self.data

    def __len__(self) -> int:
        return len(self.data)


class LinksQueue(UserDict):
    """Deque of urls.
    Only normalized urls stored.
    """

    def __init__(self, base_url=None) -> None:
        self.base_url = base_url
        super().__init__()

    def add(self, link: str) -> bool:
        if self.base_url and not link.startswith(self.base_url):
            return False
        norm_url = normalize_url(link)
        if norm_url in self.data:
            return False
        self.data[norm_url] = link
        return True

    def __lshift__(self, link: str) -> bool:
        return self.add(link)

    def add_multiple(self, links: Iterable) -> int:
        return sum(self.add(link) for link in links)

    def __contains__(self: object, link: str) -> bool:
        return normalize_url(link) in self.data

    def pop(self) -> str:
        _, link = self.data.popitem()
        return link

    def iter_pop_count(self, count: int) -> Generator:
        while self.data and count:
            yield self.pop()
            count -= 1

    def pop_count(self, count: int):
        return list(self.iter_pop_count(count))
