from abc import ABC, abstractmethod


class VacancyStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем вакансий.
    """

    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Метод для добавления вакансии в хранилище.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """
        Метод для получения вакансий из хранилища по указанным критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """
        Метод для удаления вакансии из хранилища.
        """
        pass


import json
import os


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_name='vacancies_user.json'):
        """
        Инициализация хранилища вакансий.

        :param file_name: Имя файла для хранения вакансий.
        """
        self.file_name = file_name
        self.vacancies = self.load_vacancies()

    def load_vacancies(self):
        """
        Загрузка вакансий из JSON-файла.
        """
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []


    def save_vacancies(self):
        """
        Сохранение вакансий в JSON-файл.
        """
        # Определяем путь к папке 'data' относительно корня проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')

        # Проверяем наличие директории 'data' и создаем, если она отсутствует
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Определяем полный путь к файлу vacancy_user.json
        file_path = os.path.join(data_dir, self.file_name)

        # Сохранение вакансий в JSON-файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.vacancies, f, ensure_ascii=False, indent=4)

        print(f"Вакансии сохранены в файл: {file_path}")

    def add_vacancy(self, vacancy):
        """
        Добавление вакансии в хранилище с проверкой на дублирование по ID.

        :param vacancy: Вакансия, которую нужно добавить.
        """
        # Проверка на дублирование по ID
        existing_vacancy = next((v for v in self.vacancies if v.get('id') == vacancy.get('id')), None)

        if existing_vacancy:
            print(f"Вакансия с ID {vacancy.get('id')} уже существует и не будет добавлена.")
        else:
            self.vacancies.append(vacancy)
            self.save_vacancies()
            print(f"Вакансия с ID {vacancy.get('id')} добавлена в хранилище.")

    def get_vacancies(self, criteria):
        """
        Получение вакансий по заданным критериям.

        :param criteria: Критерии поиска вакансий.
        :return: Список вакансий, соответствующих критериям.
        """
        return [vacancy for vacancy in self.vacancies if criteria in vacancy['title']]

    def delete_vacancy(self, vacancy_id):
        """
        Удаление вакансии из хранилища по ID.

        :param vacancy_id: ID вакансии для удаления.
        """
        self.vacancies = [vacancy for vacancy in self.vacancies if vacancy.get('id') != vacancy_id]
        self.save_vacancies()


# # Пример вакансий
# vacancy1 = {
#     'id': 1,
#     'title': 'Python Developer',
#     'url': 'https://example.com/vacancy/1',
#     'salary_from': 100000,
#     'salary_to': 150000,
#     'description': 'Требуется опыт работы с Python.'
# }
#
# vacancy2 = {
#     'id': 2,
#     'title': 'Java Developer',
#     'url': 'https://example.com/vacancy/2',
#     'salary_from': 120000,
#     'salary_to': 170000,
#     'description': 'Требуется опыт работы с Java.'
# }
#
# vacancy3 = {
#     'id': 2,
#     'title': 'Java Developer',
#     'url': 'https://example.com/vacancy/2',
#     'salary_from': 120000,
#     'salary_to': 170000,
#     'description': 'Требуется опыт работы с Java.'
# }
#
# # Создание экземпляра хранилища вакансий
# storage = JSONVacancyStorage()
#
# # Добавление вакансий
# storage.add_vacancy(vacancy1)
# storage.add_vacancy(vacancy2)
#
# # Получение вакансий по критериям
# print(storage.get_vacancies('Python'))
#
# # Удаление вакансии
# # storage.delete_vacancy(1)
#
# # Проверка оставшихся вакансий
# print(storage.get_vacancies(''))
#
# storage.add_vacancy(vacancy3)


