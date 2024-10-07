import json
import os
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class VacancyFileHandler(ABC):
    """
    Абстрактный класс для работы с файлами вакансий
    """

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        pass


class JSONVacancyFileHandler(VacancyFileHandler):
    """
    Класс для работы с JSON файлами
    """

    def __init__(self, file_name='vacancies.json'):
        self.file_name = os.path.join(os.getcwd(), 'data', file_name)
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        print(f"[DEBUG] Инициализирован файл: {self.file_name}")

    def add_vacancies(self, vacancies):
        """
        Добавляет вакансии в JSON файл, проверяя дубли по id
        """
        current_vacancies = self.get_vacancies()
        print(f"[DEBUG] Текущие вакансии: {current_vacancies}")  # Отладка текущих вакансий

        # Проверка, что current_vacancies - это список
        if not isinstance(current_vacancies, list):
            print("[ERROR] Текущие вакансии не являются списком, сброс значений.")
            current_vacancies = []  # Сбрасываем в пустой список

        # Используем ключ `id` для словаря
        vacancy_ids = {vac['id'] for vac in current_vacancies if isinstance(vac, dict) and 'id' in vac}

        new_vacancies = [vac.to_list() for vac in vacancies if vac.id not in vacancy_ids]

        print(f"[DEBUG] Новые вакансии для добавления: {new_vacancies}")  # Отладка новых вакансий

        current_vacancies.extend(new_vacancies)

        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(current_vacancies, f, ensure_ascii=False, indent=4)
                print(f"[DEBUG] Вакансии успешно сохранены в {self.file_name}")
        except Exception as e:
            print(f"[ERROR] Не удалось сохранить файл: {e}")

    def get_vacancies(self, criteria=None):
        """
        Получает вакансии из JSON файла, с возможностью фильтрации
        """
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as f:
                vacancies = json.load(f)
                print(f"[DEBUG] Получено {len(vacancies)} вакансий из файла.")  # Отладка количества вакансий

                if criteria:
                    # Убедитесь, что элементы - это словари, перед применением .get()
                    filtered_vacancies = [
                        vac for vac in vacancies
                        if isinstance(vac, dict) and any(
                            criteria.lower() in str(value).lower()
                            for value in vac.values()
                        )
                    ]
                    print(f"[DEBUG] Найдено {len(filtered_vacancies)} вакансий по критерию '{criteria}'.")  # Отладка фильтрации
                    return filtered_vacancies
                return vacancies

        print("[DEBUG] Файл не найден, возвращаем пустой список.")  # Отладка отсутствия файла
        return []

    def remove_vacancy(self, vacancy_url):
        """
        Удаляет вакансию по URL
        """
        vacancies = self.get_vacancies()
        print(f"[DEBUG] Количество вакансий перед удалением: {len(vacancies)}")  # Отладка перед удалением
        vacancies = [vac for vac in vacancies if vac[2] != vacancy_url]  # vac[2] — это URL вакансии
        print(f"[DEBUG] Количество вакансий после удаления: {len(vacancies)}")  # Отладка после удаления

        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
                print(f"[DEBUG] Обновленный список вакансий сохранен в {self.file_name}.")
        except Exception as e:
            print(f"[ERROR] Не удалось сохранить файл: {e}")

    def clear_vacancies(self):
        """
        Очищает файл вакансий
        """
        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)  # Сохраняем пустой список
                print(f"[DEBUG] Файл {self.file_name} успешно очищен.")
        except Exception as e:
            print(f"[ERROR] Не удалось очистить файл: {e}")


