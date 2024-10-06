from src.hh_api_abstract import HH
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


def user_interaction():
    hh = HH()
    storage = JSONVacancyStorage()

    while True:
        print("\n1. Ввести поисковый запрос для поиска вакансий")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Выйти")
        choice = input("\nВыберите действие: ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            hh.load_vacancies(keyword)
            for vac in hh.vacancies:
                vacancy = Vacancy(title=vac['name'],
                                  url=vac['alternate_url'],
                                  salary_from=vac['salary']['from'] if vac['salary'] else 0,
                                  salary_to=vac['salary']['to'] if vac['salary'] else 0,
                                  description=vac['snippet']['requirement'] if vac['snippet'] else ''
                                  )
                storage.add_vacancy(vacancy)
            print("Вакансии загружены и сохранены.")

        elif choice == '2':
            N = int(input("Введите количество вакансий для показа: "))
            sorted_vacancies = sorted([Vacancy(**vac) for vac in storage.vacancies], key=lambda v: v.salary_to, reverse=True)
            for vac in sorted_vacancies[:N]:
                print(vac)

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в описании: ")
            found_vacancies = storage.get_vacancies(keyword)
            for vac in found_vacancies:
                print(Vacancy(**vac))

        elif choice == '4':
            print("Выход.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
