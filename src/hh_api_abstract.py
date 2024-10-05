import json
import os
from abc import ABC, abstractmethod
import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий
    """

    def __init__(self):
        self.url = None
        self.headers = None
        self.params = None
        self.vacancies = []

    @abstractmethod
    def connect(self):
        """
        Метод для подключения к API, должен быть реализован в наследующем классе.
        """
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Метод для загрузки вакансий по ключевому слову, должен быть реализован в наследующем классе.
        """
        pass

    def save_vacancies(self, file_name):
        """
        Метод для сохранения вакансий в файл JSON в папку 'data'
        """
        # Определяем путь к папке 'data' относительно корня проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')

        # Проверяем наличие директории 'data' и создаем, если она отсутствует
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Определяем полный путь к файлу
        file_path = os.path.join(data_dir, file_name)

        # Сохраняем вакансии в формате JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.vacancies, f, ensure_ascii=False, indent=4)

        print(f"Вакансии сохранены в файл: {file_path}")


class HH(VacancyAPI):
    """
    Класс для работы с API HeadHunter, наследуемый от VacancyAPI
    """

    def __init__(self):
        super().__init__()
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def connect(self):
        """
        Подключение к API
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Ошибка {response.status_code}: {response.text}")

    def load_vacancies(self, keyword):
        """
        Загрузка вакансий по ключевому слову
        """
        self.params['text'] = keyword
        self.params['page'] = 0

        while self.params['page'] < 20:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                if response.status_code == 200:
                    vacancies = response.json().get('items', [])
                    if not vacancies:
                        break
                    self.vacancies.extend(vacancies)
                    self.params['page'] += 1
                else:
                    print(f"Ошибка {response.status_code}: {response.text}")
                    break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break


hh = HH()
hh.load_vacancies("Python developer")
hh.save_vacancies("vacancies.json")
