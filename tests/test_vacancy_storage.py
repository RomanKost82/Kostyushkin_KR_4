import pytest
import os
import json
from src.vacancy_storage import JSONVacancyFileHandler, Vacancy


@pytest.fixture
def setup_file_handler():
    # Создаем тестовый файл и передаем его фикстуре
    file_handler = JSONVacancyFileHandler(file_name='test_vacancies.json')
    yield file_handler
    # После завершения тестов удаляем тестовый файл
    if os.path.exists(file_handler.file_name):
        os.remove(file_handler.file_name)


def test_add_vacancies(setup_file_handler):
    file_handler = setup_file_handler
    vacancies = [Vacancy('1', 'Test Vacancy', 'http://example.com', 1000, 2000, 'Test description')]

    file_handler.add_vacancies(vacancies)
    saved_vacancies = file_handler.get_vacancies()

    assert len(saved_vacancies) == 1
    assert saved_vacancies[0][1] == 'Test Vacancy'


def test_get_vacancies(setup_file_handler):
    file_handler = setup_file_handler
    vacancies = [Vacancy('1', 'Test Vacancy', 'http://example.com', 1000, 2000, 'Test description')]
    file_handler.add_vacancies(vacancies)

    retrieved_vacancies = file_handler.get_vacancies()
    assert len(retrieved_vacancies) == 1
    assert retrieved_vacancies[0][1] == 'Test Vacancy'


def test_remove_vacancy(setup_file_handler):
    file_handler = setup_file_handler
    vacancies = [Vacancy('1', 'Test Vacancy', 'http://example.com', 1000, 2000, 'Test description')]
    file_handler.add_vacancies(vacancies)

    file_handler.remove_vacancy('http://example.com')
    remaining_vacancies = file_handler.get_vacancies()

    assert len(remaining_vacancies) == 0


def test_clear_vacancies(setup_file_handler):
    file_handler = setup_file_handler
    vacancies = [Vacancy('1', 'Test Vacancy', 'http://example.com', 1000, 2000, 'Test description')]
    file_handler.add_vacancies(vacancies)

    file_handler.clear_vacancies()
    remaining_vacancies = file_handler.get_vacancies()

    assert len(remaining_vacancies) == 0
