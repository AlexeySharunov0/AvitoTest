import allure
import pytest

from UI.tests.main_page.conftest import main_page


@pytest.mark.ui
@allure.issue(
        "https://github.com/avito-tech/tech-internship/tree/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2025",
        "Поиск задачи")
class TestMainSearchTasks:

    @allure.title("Поиск задач по полному названию задачи")
    @pytest.mark.parametrize("task_name", [
        "Адаптация карточки для мобильных устройств",
        "Оптимизация загрузки медиа-контента",
        "Добавление микроанимаций интерфейса"
    ])
    def test_search_tasks_by_name(self, main_page, task_name):
        with allure.step(f"Выполняем поиск задачи: '{task_name}'"):
            main_page.search_input.fill(task_name)

        with allure.step("Проверяем, что поиск дал результаты"):
            assert main_page.task_names.are_visible(), \
                f"Результаты поиска по запросу '{task_name}' не отображаются"

        with allure.step("Проверяем, что найденная задача соответствует запросу"):
            found_text = main_page.task_names.get_texts()
            assert task_name in found_text, \
                f"Задача '{task_name}' не найдена. Найдено: {found_text}"

    @allure.title("Поиск задач по полному названию задачи")
    @pytest.mark.parametrize("task_name", [
        "Адаптация карточ",
        "Оптимизация заг",
        "Добавление микроан"
    ])
    def test_search_tasks_by_part_name(self, main_page, task_name):
        with allure.step(f"Выполняем поиск задачи: '{task_name}'"):
            main_page.search_input.fill(task_name)

        with allure.step("Проверяем, что поиск дал результаты"):
            assert main_page.task_names.are_visible(), \
                f"Результаты поиска по запросу '{task_name}' не отображаются"

        with allure.step("Проверяем, что найденная задача соответствует запросу"):
            found_texts = main_page.task_names.get_texts()
            for found_text in found_texts:
                assert task_name in found_text, \
                    f"Частичное название '{task_name}' не найдено в задаче '{found_text}'"

    @allure.title("Поиск с максимальной длиной запроса")
    def test_search_tasks_max_length_query(self, main_page):
        long_query = "test" * 100
        with allure.step(f"Ввести запрос длиной {len(long_query)} символов"):
            main_page.search_input.fill(long_query)
        with allure.step("Проверить обработку длинного запроса"):
            assert main_page.not_found_text.is_visible(), "Текст 'Задачи не найдены' отображается"

    @allure.title("Поиск с пустым запросом")
    def test_search_tasks_min_length_query(self, main_page):
        with allure.step("Ввести пробелы в поисковое поле"):
            main_page.search_input.fill("            ")
        with allure.step("Проверить обработку коротког запроса"):
            assert main_page.not_found_text.is_visible(), "Текст 'Задачи не найдены' отображается"


    @allure.title("Поиск задач по исполнителю '{executor_name}'")
    @pytest.mark.parametrize("executor_name,expected_tasks", [
        ("Илья Романов", {
            "Адаптация карточки для мобильных устройств",
            "Оптимизация работы с API",
            "Оптимизация бандла Webpack",
            "цу",
            "Оптимизация загрузки медиа-контента",
            "Реализация новой галереи изображений",
            "Уменьшение времени First Contentful Paint"
        }),
        ("Ольга Новикова", {
            "Интеграция с CI/CD",
            "Интеграция с Allure отчетностью",
        }),
    ])
    def test_search_tasks_by_executor(self, main_page, executor_name, expected_tasks):
        with allure.step(f"Вводим в поисковое поле имя исполнителя '{executor_name}'"):
            main_page.search_input.fill(executor_name)

        with allure.step(f"Проверяем, что отображаются результаты поиска для '{executor_name}'"):
            assert main_page.task_names.are_visible(), f"Задачи не отображаются при поиске по исполнителю '{executor_name}'"

        with allure.step(f"Получаем названия всех найденных задач для '{executor_name}'"):
            found_tasks = main_page.task_names.get_texts()
            found_tasks_set = {text.strip() for text in found_tasks}

        with allure.step(f"Проверяем, что для исполнителя '{executor_name}' найдены только ожидаемые задачи"):
            assert found_tasks_set == expected_tasks, (
                f"Ожидались задачи: {expected_tasks}, "
                f"но найдены: {found_tasks_set}"
            )

    @allure.title("Поиск несуществующих задач")
    def test_search_tasks_by_invalid_name(self, main_page):
        with allure.step(f"Выполняем поиск задачи:"):
            main_page.search_input.fill("test_invalid_task_name")
        with allure.step("Проверяем, что поиск дал результаты"):
            assert main_page.task_names.are_not_visible(), \
                f"Результаты поиска по запросу отображаются"
        with allure.step("Текст заглушка отображдается"):
            assert main_page.not_found_text.is_visible(), "Текст 'Задачи не найдены' отображается"

    @allure.title("Поиск с учетом регистра")
    @pytest.mark.parametrize("search_query, expected_task", [
        ("ДоБаВлЕНие МикроАнимаций", "Добавление микроанимаций интерфейса"),
        ("ОптИмиЗация ЗагрУзКи", "Оптимизация загрузки медиа-контента"),
    ])
    def test_search_tasks_with_register(self, main_page, search_query, expected_task):
        with allure.step(f"Выполняем поиск задачи: '{search_query}'"):
            main_page.search_input.fill(search_query)
        with allure.step("Проверяем, что поиск дал результаты"):
            assert main_page.task_names.are_visible(), \
                f"Результаты поиска по запросу '{search_query}' не отображаются"
        with allure.step("Проверяем, что найденная задача соответствует запросу"):
            found_texts = main_page.task_names.get_texts()
            assert any(search_query.lower() in text.lower() for text in found_texts), \
                f"Задача '{search_query}' не найдена. Найдено: {found_texts}"

    @allure.title("Очистка поля поиска с помощью иконки крестика")
    def test_clear_search_field_with_icon(self, main_page):
        search_text = "Тестовый запрос"

        with allure.step(f"Вводим текст в поле поиска: '{search_text}'"):
            main_page.search_input.fill(search_text)
            assert main_page.search_input.get_attribute("value") == search_text, \
                f"Поле поиска должно содержать '{search_text}'"

        with allure.step("Нажимаем на иконку крестика для очистки поля"):
            main_page.search_clear_icon.click()

        with allure.step("Проверяем, что поле поиска пустое"):
            value_after_clear = main_page.search_input.get_attribute("value")
            assert value_after_clear == "", \
                f"Поле поиска должно быть пустым после очистки, но содержит: '{value_after_clear}'"


