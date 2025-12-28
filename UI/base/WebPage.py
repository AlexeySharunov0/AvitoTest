import logging
import time

from playwright.sync_api import Page, Locator

from UI.base.WebElement import WebElement

logger = logging.getLogger(__name__)


class WebPage:
    def __init__(self, page: Page):
        self._page = page
        self.context = page.context

    @property
    def url(self) -> str:
        return self._page.url

    def get_page(self, link: str) -> None:
        """
        Перейти по ссылке на страницу
        Args:
            link: (str) ссылка
        """
        logger.info(f'Переходим по ссылке {link}')
        self._page.goto(link)