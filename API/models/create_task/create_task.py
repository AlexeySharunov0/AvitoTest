import requests
import allure

from API.data.tasks import Model


BASE_URL = 'https://enchanting-dream.onrender.com/api/v1/'

class CreateTaskUrls:
    '''
    ссылки на свагер нет(((
    '''

    # Создание новой задачи
    CREATE = 'tasks/create'

    # Получение всех задач
    TASKS = 'tasks/'

    # Получение новой созданной задачи
    NEW_TASKS = 'tasks/{}'  # придумать, как потом описать эту ручку



class CreateTask(CreateTaskUrls):

    @allure.step('Создание новой задачи')
    def create_task(self, task_data):
        url = BASE_URL + 'tasks/create'
        return requests.post(url, json=task_data)

    @allure.step('Получение всех задач')
    def get_all_tasks(self):
        url = BASE_URL + 'tasks'
        response = requests.get(url)

        Model(data=response.json()['data'])

        return response

    @allure.step('Получение задачи по ID')
    def get_task_by_id(self, task_id):
        url = BASE_URL + f'tasks/{task_id}'
        return requests.get(url)