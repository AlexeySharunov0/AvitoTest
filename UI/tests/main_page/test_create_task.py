import allure
import pytest

from UI.tests.main_page.conftest import main_page

@allure.issue(
    "https://github.com/avito-tech/tech-internship/tree/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2025",
    "Создание задачи")
@pytest.mark.ui
class TestMainCreateTasksUI():

    @allure.title("Окно создания задачи отображается")
    def test_create_task_window_is_visible(self, main_page):
        with allure.step("Открыть окно создания задачи"):
            main_page.create_task_button.click()
        with allure.step("Окно появилось"):
            assert main_page.create_task_window.is_visible(), "Окно создания задачи не появилось"

    @allure.title("Создание задачи через UI")
    def test_create_task_final(self, main_page):
        task_title = main_page.create_task()

        with allure.step(f"Проверяем, что задача '{task_title}' создалась"):
            main_page.search_input.fill(task_title)

            found_tasks = main_page.task_names.get_texts()
            assert task_title in found_tasks, \
                f"Задача '{task_title}' не найдена. Найдено: {found_tasks}"



