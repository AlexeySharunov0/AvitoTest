import allure
import pytest

from API.models.create_task.create_task import CreateTask
from API.utils.generate import Gen


@pytest.mark.api
@allure.issue(
    "https://github.com/avito-tech/tech-internship/tree/main/Tech%20Internships/QA/QA-trainee-assignment-autumn-2025",
    "Создание задачи")
class TestCreateTaskAPI(CreateTask):

    @allure.title("Создание задачи и проверка её наличия в списке всех задач")
    def test_create_task_and_verify_in_list(self):
        unique_title = Gen.generate_title_with_datetime("API Test")
        unique_description = f"API Test Description {Gen.generate_text(8, lang='eng')}"

        task_data = {
            "title": unique_title,
            "description": unique_description,
            "priority": "Low",
            "assigneeId": 3,
            "boardId": 1
        }

        with allure.step(f"Создаём новую задачу"):
            create_resp = self.create_task(task_data)
            assert create_resp.status_code == 200
            task_id = create_resp.json()["data"]["id"]

        with allure.step(f"Проверяем, что задача есть в списке всех задач"):
            all_tasks = self.get_all_tasks().json()["data"]
            found = next(task for task in all_tasks if task["id"] == task_id)

            assert found["title"] == unique_title
            assert found["description"] == unique_description
            assert found["priority"] == task_data["priority"]