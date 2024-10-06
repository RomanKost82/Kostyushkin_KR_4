from src.hh_api_abstract import HHVacancyAPI
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyFileHandler


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль
    """
    api = HHVacancyAPI()
    file_handler = JSONVacancyFileHandler()

    while True:
        print("\n1. Ввести поисковый запрос для вакансий")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в любом поле")
        print("4. Удалить вакансию по ID")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            vacancies = api.get_vacancies(keyword)
            print(f"[DEBUG] Получено {len(vacancies)} вакансий по запросу '{keyword}'.")

            if not vacancies:  # Проверяем, что вакансии получены
                print("Не удалось получить вакансии, попробуйте еще раз.")
                continue

            vacancy_objects = []
            for vac in vacancies:
                if vac is not None:  # Проверяем, что vac не None
                    print(f"[DEBUG] Обработка вакансии: {vac}")  # Отладка текущей вакансии

                    salary_data = vac.get('salary')  # Получаем salary

                    if salary_data is not None:  # Проверяем, что salary не None
                        salary_from = salary_data.get('from', 0)  # Получаем 'from' для зарплаты
                        salary_to = salary_data.get('to', 0)  # Получаем 'to' для зарплаты
                    else:
                        salary_from = 0  # Значение по умолчанию, если salary равно None
                        salary_to = 0  # Значение по умолчанию, если salary равно None

                    description = vac.get('snippet', {}).get('requirement', '')
                    vacancy_objects.append(Vacancy(
                        vac['id'],
                        vac['name'],
                        vac['alternate_url'],
                        salary_from,
                        salary_to,
                        description
                    ))
                else:
                    print("[DEBUG] Получена пустая вакансия (None).")  # Отладочное сообщение

            print(
                f"[DEBUG] Создано {len(vacancy_objects)} объектов вакансий.")  # Количество созданных объектов вакансий
            if vacancy_objects:  # Проверяем, что список не пуст
                file_handler.add_vacancies(vacancy_objects)
                print("Вакансии добавлены в файл.")
            else:
                print("Нет вакансий для добавления.")


        elif choice == '2':
            top_n = int(input("Введите количество вакансий для отображения: "))
            vacancies = file_handler.get_vacancies()

            # Инициализация списка для объектов вакансий
            vacancy_objects = []

            # Перебор вакансий и создание объектов Vacancy
            for vac in vacancies:

                # Проверяем, что vac - это список и содержит ожидаемые данные
                if isinstance(vac, list) and len(vac) >= 6:
                    try:
                        salary_from = vac[3] if vac[3] is not None else 0  # Зарплата от
                        salary_to = vac[4] if vac[4] is not None else 0  # Зарплата до
                        vacancy_objects.append(Vacancy(
                            vac[0],  # ID
                            vac[1],  # Название
                            vac[2],  # URL
                            salary_from,
                            salary_to,
                            vac[5]  # Описание
                        ))

                    except IndexError:

                        print("[ERROR] Не хватает данных в вакансии.")

            # Сортировка по зарплате
            sorted_vacancies = sorted(vacancy_objects, key=lambda x: x.salary_from, reverse=True)[:top_n]

            # Вывод отсортированных вакансий
            for vac in sorted_vacancies:
                print(f"Название: {vac.title}, Зарплата: {vac.salary_from}-{vac.salary_to}, Ссылка: {vac.url}")



        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = file_handler.get_vacancies()
            matching_vacancies = []

            for vac in vacancies:
                # Проверяем, что vac - это список и что ключевое слово присутствует в любом из элементов
                if isinstance(vac, list) and any(keyword.lower() in str(item).lower() for item in vac):
                    matching_vacancies.append(vac)

            if not matching_vacancies:
                print("Вакансии не найдены по данному критерию.")
            else:
                for vac in matching_vacancies:
                    print(f"Название: {vac[1]}, Зарплата: {vac[3]}-{vac[4]}, Ссылка: {vac[2]}")


        elif choice == '4':
            vacancy_id = input("Введите ID вакансии для удаления: ")
            file_handler.remove_vacancy(vacancy_id)
            print(f"Вакансия с ID {vacancy_id} удалена.")

        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
