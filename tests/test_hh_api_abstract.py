import pytest
from src.hh_api_abstract import HHVacancyAPI
from unittest.mock import patch

# Мокаем запросы, чтобы не обращаться к реальному API
@patch('src.hh_api_abstract.requests.get')
def test_get_vacancies(mock_get):
    # Настраиваем mock объект
    mock_response = {
        'items': [
            {'id': '1', 'name': 'Test Vacancy 1', 'alternate_url': 'http://example.com/1', 'salary': {'from': 1000, 'to': 2000}, 'snippet': {'requirement': 'Requirement 1'}},
            {'id': '2', 'name': 'Test Vacancy 2', 'alternate_url': 'http://example.com/2', 'salary': {'from': 3000, 'to': None}, 'snippet': {'requirement': 'Requirement 2'}}
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api = HHVacancyAPI()
    vacancies = api.get_vacancies('тест')

    # Проверяем, что правильно получены вакансии
    assert len(vacancies) == 2
    assert vacancies[0]['id'] == '1'
    assert vacancies[0]['salary']['from'] == 1000
    assert vacancies[1]['salary']['to'] is None
