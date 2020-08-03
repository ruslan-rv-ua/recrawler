"""Containers module."""

from collections import UserDict
from urllib.parse import urldefrag


def normalize_url(url: str) -> str:
    """Removes from url fragment and trailing slash

    :param url: url to normalize
    :type url: str
    :return: normalized url
    :rtype: str
    """
    return urldefrag(url).url.rstrip('/')


class LinksDeque(UserDict):
    """Deque of urls.
    Only normalized urls stored.
    """

    def __init__(self) -> None:
        super().__init__()

    def add(self, link: str) -> bool:
        norm_url = normalize_url(link)
        if norm_url in self.data:
            return False
        self.data[norm_url] = link
        return True

    def __lshift__(self, link: str) -> bool:
        return self.add(link)

    def __contains__(self, link: str) -> bool:
        return normalize_url(link) in self.data

    def pop(self) -> str:
        norm_link, link = self.data.popitem()
        return link

    def iter_pop_count(self, count: int):  # TODO: typinig.Generator
        while self.data and count:
            yield self.pop()
            count -= 1

    def pop_count(self, count: int):
        return list(self.iter_pop_count(count))
