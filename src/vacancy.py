class Vacancy:
    __slots__ = ['id', 'title', 'url', 'salary_from', 'salary_to', 'description']

    def __init__(self, id, title, url, salary_from=0, salary_to=0, description=''):
        self.id = id
        self.title = title
        self.url = url
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.description = description

    @staticmethod
    def _validate_salary(salary):
        if salary is None or isinstance(salary, (int, float)) and salary >= 0:
            return salary
        raise ValueError("Зарплата должна быть положительным числом или None.")

    def __lt__(self, other):
        return self.salary_to < other.salary_to

    def __le__(self, other):
        return self.salary_to <= other.salary_to

    def __eq__(self, other):
        return self.salary_to == other.salary_to

    def __repr__(self):
        return f"{self.title} ({self.salary_from}-{self.salary_to} руб.): {self.url}"

    def to_list(self):
        return [
            self.id,
            self.title,
            self.url,
            self.salary_from,
            self.salary_to,
            self.description
        ]
