from UI.base.WebElement import WebElement, ManyWebElements


class MainPageLocators:

    def __init__(self, page):

        ### Поиск

        # Строка поиска
        self.search_input = WebElement(page, "//*[@placeholder='Поиск']")

        # Текст 'Задачи не найдены'
        self.not_found_text = WebElement(page, "//*[text()='Задачи не найдены']")

        # Задача 'Адаптация карточки для мобильных устройств'
        self.task_adaptation = WebElement(page, "//*[text()='Адаптация карточки для мобильных устройств']")

        # Задача 'Оптимизация загрузки медиа-контента'
        self.task_media = WebElement(page, "//*[text()='Оптимизация загрузки медиа-контента']")

        # Задача 'Добавление микроанимаций интерфейса'
        self.task_micro = WebElement(page, "//*[text()='Добавление микроанимаций интерфейса']")

        # Названия задач
        self.task_names = ManyWebElements(page, ".MuiTypography-root.MuiTypography-subtitle1.css-12sszql")

        # Иконка крестика (в поле поиска)
        self.search_clear_icon = WebElement(page, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeSmall.css-xz9haa")


        ### Создание задачи

        # Кнопка 'Создать задачу'
        self.create_task_button = WebElement(page, "//*[text()='Создать задачу']")

        # Окно создания задачи
        self.create_task_window = WebElement(page, ".MuiBox-root.css-1epuubg")

        # Поле ввода - название задачи
        self.task_name_input = WebElement(page, ".MuiInputBase-input.MuiOutlinedInput-input.css-1pk1fka")

        # Поле ввода - описание задачи
        self.task_description_input = WebElement(page, "(//*[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputMultiline css-s63k3s'])[1]")

        # Комбобокс - проект
        self.project_combobox = WebElement(page, "(//*[contains(@class, 'MuiSelect-select')])[3]")

        # Комбобокс - приоритет
        self.priority_combobox = WebElement(page, "(//*[contains(@class, 'MuiSelect-select')])[4]")

        # Комбобокс - исполнитель
        self.executor_combobox = WebElement(page, "(//*[contains(@class, 'MuiSelect-select')])[6]")

        # Комбобокс - статус
        self.status_combobox = WebElement(page, "(//*[contains(@class, 'MuiSelect-select')[5]")

        # Кнопка 'Создать' (в окне создания задачи)
        self.create_task_button_in_window = WebElement(page, "//*[text()='Создать']")

        # Варианты выбора в комбо-боксах (первый)
        self.combobox_options = WebElement(page, "(//*[@class='MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-5dycmn'])[1]")

