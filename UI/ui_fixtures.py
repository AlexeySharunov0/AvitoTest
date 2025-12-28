# UI/ui_fixtures.py

import os
import allure
import pytest
from playwright.sync_api import Playwright, Browser
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

IS_HEADLESS = False if os.getenv('IS_HEADLESS') == 'FALSE' else True # если надо в хедлесс режиме, то поменят первый False на True


# ====================================================== Настройки =====================================================

@pytest.fixture(scope="session")
def browser_context_args() -> dict:
    """Настройки контекста браузера"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "ru-Ru",
        "timezone_id": "Europe/Moscow"
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(request) -> dict:
    """Настройки запуска браузера"""
    browser_name = request.config.getoption("--browser", default="chromium")
    headless = IS_HEADLESS

    args = []
    if browser_name in ["chromium", "chrome"]:
        args.append("--disable-dev-shm-usage")  # Только для Chromium, внимательнее пжлст

    return {
        "headless": headless,
        "slow_mo": 200,
        "args": args
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, browser_type_launch_args: dict, request) -> Browser:
    try:
        browser = playwright.chromium.launch(
            channel="chrome",
            **browser_type_launch_args
        )
    except Exception as e:
        browser = playwright.chromium.launch(**browser_type_launch_args)
    return browser

@pytest.fixture(scope="session")
def browser_context(browser, browser_context_args) -> Browser:
    """Один контекст на сессию, использует общий браузер"""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context) -> None:
    """Новая страница на каждый тест"""
    page = browser_context.new_page()
    page.set_default_timeout(10000)
    yield page
    page.close()


# ====================================================== Debugging =====================================================

def screenshot_on_failure(page, request):
    """Скриншот при падении теста"""
    if request.session.testsfailed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(screenshots_dir, f"{request.function.__name__}_{timestamp}.png")

        page.screenshot(path=screenshot_path)
        logger.warning(f"Скриншот сохранён: {screenshot_path}")

        with open(screenshot_path, 'rb') as image_file:
            allure.attach(
                image_file.read(),
                name=request.function.__name__,
                attachment_type=allure.attachment_type.PNG
            )
