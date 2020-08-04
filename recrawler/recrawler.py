"""Main module."""

import logging

from async_get_web import get_webpages

from .containers import LinksQueue, LinksSet

DEFAULT_THREADS = 1


class Crawler:
    def __init__(self, link: str, *, base_url=None, threads: int = DEFAULT_THREADS, logger: logging.Logger = None) -> None:
        self.link = link
        self.base_url = base_url if base_url else link
        self.threads = threads
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

    def crawl(self) -> None:
        seen_links = LinksSet()
        links_queue = LinksQueue(base_url=self.base_url)
        links_queue.add(self.link)
        self.logger.info(f'Crawling started')
        collected_urls_count = 0
        while links_queue:
            links_to_get = links_queue.pop_count(self.threads)
            self.logger.info(
                f'Collected: {collected_urls_count}. Enqueued: {len(links_queue)}. Getting: {len(links_to_get)}')
            webpages = [webpage for webpage in get_webpages(
                links_to_get) if webpage.error is None]
            for webpage in webpages:
                actual_url = webpage.url
                if actual_url in seen_links:
                    continue
                seen_links.add(actual_url)
                yield webpage
                collected_urls_count += 1

                # collect links
                try:
                    links = webpage.response.html.absolute_links
                except ValueError:
                    self.logger.debug(
                        f'Error parsing absolute links: {webpage.response.url}')
                    continue
                links_queue.add_multiple(
                    link for link in links if link not in seen_links)

            # also mark as seen all gotten links
            seen_links.add_multiple(links_to_get)

        self.logger.info(
            f'Crawling finished. {collected_urls_count} links found')

    def __iter__(self):
        yield from self.crawl()
