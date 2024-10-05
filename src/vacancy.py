class Vacancy:
    __slots__ = ['title', 'url', 'salary_from', 'salary_to', 'description']

    def __init__(self, title, url, salary_from=None, salary_to=None, description=""):
        """
        Инициализация объекта вакансии.

        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary_from: Минимальная зарплата (может быть None)
        :param salary_to: Максимальная зарплата (может быть None)
        :param description: Описание или требования к вакансии
        """
        self.title = title
        self.url = url
        self.salary_from = self.validate_salary(salary_from)
        self.salary_to = self.validate_salary(salary_to)
        self.description = description

    def validate_salary(self, salary):
        """
        Метод для валидации зарплаты. Если зарплата не указана, возвращает 0.
        """
        if salary is None:
            return 0
        if isinstance(salary, (int, float)) and salary >= 0:
            return salary
        else:
            raise ValueError("Зарплата должна быть положительным числом или None.")

    def __str__(self):
        """
        Метод для текстового представления вакансии.
        """
        salary_info = f"от {self.salary_from} до {self.salary_to}" if self.salary_from and self.salary_to else "Зарплата не указана"
        return f"Вакансия: {self.title}\nСсылка: {self.url}\nЗарплата: {salary_info}\nОписание: {self.description}"

    def __eq__(self, other):
        """
        Сравнение вакансий по зарплате. Вакансии считаются равными, если у них одинаковая минимальная зарплата.
        """
        if isinstance(other, Vacancy):
            return self.salary_from == other.salary_from
        return False

    def __lt__(self, other):
        """
        Сравнение вакансий по минимальной зарплате. Возвращает True, если у текущей вакансии зарплата меньше, чем у другой.
        """
        if isinstance(other, Vacancy):
            return self.salary_from < other.salary_from
        return False

    def __le__(self, other):
        """
        Сравнение вакансий по минимальной зарплате. Возвращает True, если у текущей вакансии зарплата меньше или равна другой.
        """
        return self < other or self == other


# Пример использования
vacancy1 = Vacancy("Python", "https://hh.ru/vacancy/123456", 100000, 150000,
                   "Требования: знание Python, Django")
vacancy2 = Vacancy("Junior Python Developer", "https://hh.ru/vacancy/654321", 70000, 100000,
                   "Требования: базовые знания Python")

print(vacancy1)
print(vacancy2)

# Сравнение вакансий
# print(vacancy1 > vacancy2)  # True, так как у vacancy1 зарплата выше
