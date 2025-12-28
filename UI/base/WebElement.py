import logging
from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError

logger = logging.getLogger(__name__)


class WebElement:
    def __init__(self, page: Page, locator: str = None, element: Locator = None):
        self._page = page
        self.locator = locator
        self.element = self._page.locator(locator).nth(0) if element is None else element
        self.logging_name = f'<{locator}>'
        self._timeout = 30000

    def __getitem__(self, item: int) -> "WebElement":
        """
        Перегрузка операции получения элемента по индексу
        Args:
            item: (int) порядковый номер элемента

        Returns: (WebElement) новая сущность элемента под указанным порядковым номером

        """
        return WebElement(self._page, locator=self.locator, element=self._page.locator(self.locator).nth(item))

    def check_element(self) -> None:
        """
        Проверка, что элемент присутствует на странице
        """
        try:
            self._page.wait_for_selector(self.locator, timeout=self._timeout)
        except TimeoutError as e:
            logger.error(f'Элемент {self.logging_name} не найден')
            raise e

    def get_text(self) -> str:
        """
        Получить текст элемента
        Returns: (str) текст
        """
        logger.info(f'Получаем текст элемента {self.logging_name}')

        return self.element.inner_text()

    def fill(self, text: str, clear: bool = True) -> None:
        """
        Ввод данных через insert в любое поле
        Args:
            text: (str) текст, который требуется ввести
            clear: (bool) если True, поле будет очищено перед вводом текста
        """
        logger.info(f'Вводим текст {text} в элемент {self.logging_name}')

        if clear:
            self.element.fill(text)
        else:
            current_value = self.element.evaluate('el => el.value')
            new_value = f"{current_value}{text}"
            self.element.fill(new_value)

    def is_visible(self) -> bool:
        """
        Проверка, что элемент виден
        Returns: True если элемент виден, False иначе
        """
        logger.info(f'Проверяем, что элемент {self.logging_name} виден')
        try:
            self.check_element()
            expect(self.element).to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Элемент {self.logging_name} не виден')
            return False
        except TimeoutError:
            return False

    def get_attribute(self, attribute_name: str) -> str:
        """
        Получить значение атрибута элемента
        Args:
            attribute_name: (str) название атрибута (class, type, id etc.)

        Returns: (str) значение атрибута
        """
        logger.info(f'Получаем значение атрибута {attribute_name} у элемента {self.logging_name}')

        return self.element.get_attribute(attribute_name)

    def click(self, amount: int = 1, force: bool = False) -> None:
        """
        Клик по элементу
        """
        logger.info(f'Кликаем по элементу {self.logging_name}')
        self.element.click(click_count=amount, timeout=self._timeout, force=force)

    def clear(self) -> None:
        """
        Очистить инпут элемента
        """
        logger.info('Очищаем инпут элемента')

        self.element.clear()


class ManyWebElements:
    def __init__(self, page: Page, locator: str = None, elements: Locator = None):
        self._page = page
        self.locator = locator
        self.elements = self._page.locator(locator) if elements is None else elements
        self.logging_name = f'<{locator}>'
        self._timeout = 5000

    def __getitem__(self, item: int) -> WebElement:
        """
        Перегрузка операции итерирования по элементам
        Args:
            item: порядковый номер элемента

        Returns: (Locator) элемент под номером item
        """
        elements = self.get_items()

        return elements[item]

    def get_items(self) -> list[WebElement]:
        """
        Возвращает список всех элементов с типом WebElement
        Returns: список всех элементов с типом WebElement
        """
        elements = self.find()
        new_elements = []

        for index, elem in enumerate(elements):
            new_elements.append(WebElement(self._page, locator=self.locator, element=elem))

        return new_elements

    def find(self) -> list[Locator]:
        """
        Ищет элементы на странице.
        Returns: (list[Locator]) список найденных элементов
        """
        try:
            self.check_elements()
            elements = self.elements.all()
        except Exception as e:
            print(f'Элементов с локатором {self.locator} не найдено. Ошибка: {e}')
            elements = []

        return elements

    def check_elements(self) -> None:
        """
        Проверка, что элементы присутствуют на странице
        """
        try:
            self._page.wait_for_selector(self.locator, timeout=self._timeout)
        except TimeoutError as e:
            logger.error(f'Элементы {self.logging_name} не найдены')
            raise e

    def get_texts(self) -> list[str]:
        """
        Получить текст всех элементов
        Returns: (list[str]) список текстов
        """
        logger.info(f'Получаем тексты элементов {self.logging_name}')
        return [el.inner_text() for el in self.find()]

    def are_visible(self) -> bool:
        """
        Проверить, что все элементы видны
        Returns: (bool) True если все видны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} видны')
        try:
            for el in self.elements.all():
                expect(el).to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Не все элементы {self.logging_name} видны')
            return False

    def are_not_visible(self) -> bool:
        """
        Проверить, что все элементы не видны
        Returns: (bool) True если все не видны, False иначе
        """
        logger.info(f'Проверяем, что все элементы {self.logging_name} не видны')
        try:
            for el in self.elements.all():
                expect(el).not_to_be_visible()
            return True
        except AssertionError:
            logger.error(f'Некоторые элементы {self.logging_name} видны')
            return False