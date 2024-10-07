import pytest
from src.vacancy import Vacancy

def test_vacancy_creation():
    vac = Vacancy(id='1', title='Test Vacancy', url='http://example.com', salary_from=1000, salary_to=2000, description='Test description')
    assert vac.id == '1'
    assert vac.title == 'Test Vacancy'
    assert vac.salary_from == 1000
    assert vac.salary_to == 2000
    assert vac.url == 'http://example.com'

def test_vacancy_comparisons():
    vac1 = Vacancy(id='1', title='Test Vacancy 1', url='http://example.com/1', salary_from=1000, salary_to=2000)
    vac2 = Vacancy(id='2', title='Test Vacancy 2', url='http://example.com/2', salary_from=3000, salary_to=4000)

    assert vac1 < vac2
    assert vac1 <= vac2
    assert vac2 > vac1
    assert vac2 >= vac1
