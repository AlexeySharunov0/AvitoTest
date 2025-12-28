import logging

import allure
from playwright.sync_api import Page

from UI.base.WebPage import WebPage
from API.utils.generate import Gen
from UI.pages.main_page.main_page.main_page_locators import MainPageLocators

logger = logging.getLogger(__name__)


class MainPage(WebPage, MainPageLocators):
    def __init__(self, page: Page, url: str = None):
        WebPage.__init__(self, page)  # Явный вызов инициализатора WebPage
        MainPageLocators.__init__(self, page)  # Явный вызов инициализатора CanvasPageLocators
        self._page = page
        self.base_url = url if url else 'https://avito-tech-internship-psi.vercel.app/'
        self.get_page(self.base_url)

    @allure.step("Создаем задачу")
    def create_task(self, task_title=None, task_description=None):
        if not task_title:
            task_title = Gen.generate_title_with_datetime("UI Task")
        if not task_description:
            task_description = f"Description {Gen.generate_text(8)}"

        with allure.step(f"Создаем задачу '{task_title}' через UI"):
            self.create_task_button.click()

            self.task_name_input.fill(task_title)
            self.task_description_input.fill(task_description)

            self.project_combobox.click()
            self.combobox_options.click()

            self.priority_combobox.click()
            self.combobox_options.click()

            self.executor_combobox.click()
            self.combobox_options.click()

            self.create_task_button_in_window.click()

        return task_title