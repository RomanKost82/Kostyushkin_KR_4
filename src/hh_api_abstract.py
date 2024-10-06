from abc import ABC, abstractmethod
import requests



class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий
    """
    @abstractmethod
    def get_vacancies(self, keyword):
        """
        Метод для получения вакансий по ключевому слову
        """
        pass


class HHVacancyAPI(VacancyAPI):
    """
    Реализация API HeadHunter для получения вакансий
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'Vacancy-App'}

    def _make_request(self, params):
        """
        Приватный метод для отправки запроса к API hh.ru
        """
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка {response.status_code}: {response.text}")

    def get_vacancies(self, keyword):
        """
        Получение вакансий по ключевому слову
        """
        params = {'text': keyword, 'per_page': 100, 'page': 0}
        try:
            response_data = self._make_request(params)
            print(
                f"Получено {len(response_data.get('items', []))} вакансий по запросу '{keyword}'.")  # Добавляем отладочное сообщение
            return response_data.get('items', [])
        except Exception as e:
            print(f"Ошибка при получении вакансий: {e}")  # Сообщение об ошибке
            return []


# vac = HHVacancyAPI()
# b = vac.get_vacancies('машинист')

#
# for r in b:
#     print(r)

