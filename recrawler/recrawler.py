"""Main module."""

import logging
from .containers import LinksDeque
from async_get_web import get_webpages

DEFAULT_REQUESTS_AT_ONES = 1


class Crawler:
    def __init__(self, link: str, requests_at_ones: int = DEFAULT_REQUESTS_AT_ONES, logger: logging.Logger = None) -> None:
        self.link = link
        self.requests_at_ones = requests_at_ones
        self.logger = logger or self._get_logger()

    def _get_logger(self):
        FORMAT = "[{levelname}] <{funcName}():{lineno}> {message}"
        logFormatter = logging.Formatter(FORMAT, style='{')
        logger = logging.getLogger('Crawler')
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
        logger.setLevel(logging.INFO)
        return logger

    def _enqueue_link(self, link: str) -> bool:
        self.logger.debug(f"Enqueuing link: {link}")
        if link in self.seen_links:
            self.logger.debug(f'Already seen, skippiing')
            return False
        # TODO: filter foreighn links!
        self.links_queue.add(link)
        return True

    def crawl(self) -> None:
        self.seen_links = LinksDeque()
        self.links_queue = LinksDeque()
        self._enqueue_link(self.link)
        self.logger.info(f'Crawler started')
        collected_urls_count = 0  # TODO: is it needed?
        while self.links_queue:
            links_to_get = self.links_queue.pop_count(self.requests_at_ones)
            self.logger.info(
                f'Collected: {collected_urls_count}. Enqueued: {len(self.links_queue)}. Getting: {len(links_to_get)}')
            webpages = [webpage for webpage in get_webpages(
                links_to_get) if webpage.error is None]
            for webpage in webpages:
                actual_url = webpage.url
                if actual_url in self.seen_links:
                    continue
                self.seen_links.add(actual_url)
                yield webpage
                collected_urls_count += 1

                # collect links
                try:
                    links = webpage.response.html.absolute_links
                except ValueError:
                    self.logger.debug(
                        f'Error parsing absolute links: {webpage.response.url}')
                    continue
                for link in links:
                    self._enqueue_link(link)

            # also mark as seen all gotten links
            self.seen_links.add_multiple(links_to_get)
