from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import pytest

pytest_plugins = ['UI.ui_fixtures']

load_dotenv()



_playwright = None

@pytest.fixture(scope="session", autouse=True)
def global_playwright():
    """Запускает Playwright на всю сессию"""
    global _playwright
    _playwright = sync_playwright().start()
    yield _playwright
    _playwright.stop()


@pytest.fixture(scope="session")
def playwright(global_playwright):
    """Доступ к Playwright для других фикстур (например, browser)"""
    return global_playwright