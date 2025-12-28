import pytest

from UI.pages.main_page.main_page.main_page import MainPage
from UI.ui_fixtures import screenshot_on_failure






# =========================================== Главная страница продукта ================================================


@pytest.fixture
def main_page(page, request) -> MainPage:
    if hasattr(request, 'param'):
        main_page_obj = MainPage(page, request.param)
    else:
        main_page_obj = MainPage(page)

    yield main_page_obj

    screenshot_on_failure(page, request)