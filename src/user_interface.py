from src.db_manager import DBManager
from tabulate import tabulate


def print_menu() -> None:
    """
    Выводит список доступных действий для пользователя.
    """
    print("\nВыберите действие:")
    print("1. Показать компании и количество вакансий")
    print("2. Показать все вакансии")
    print("3. Показать среднюю зарплату по вакансиям")
    print("4. Показать вакансии с зарплатой выше средней")
    print("5. Поиск вакансий по ключевому слову")
    print("0. Выход")


def user_interface(db_manager: DBManager) -> None:
    """
    Запускает пользовательский интерфейс для взаимодействия с базой данных.

    :param db_manager: Экземпляр класса DBManager для работы с базой данных.
    """
    while True:
        print_menu()
        choice = input("Введите номер действия: ")

        if choice == '1':
            data = db_manager.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            print(tabulate(data, headers=["Компания", "Количество вакансий"], tablefmt="pretty"))

        elif choice == '2':
            data = db_manager.get_all_vacancies()
            print("\nВсе вакансии:")
            print(tabulate(data, headers=["Компания", "Вакансия", "Зарплата", "Ссылка"], tablefmt="pretty"))

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата по всем вакансиям: {avg_salary} руб.")

        elif choice == '4':
            data = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            print(tabulate(data, headers=["Компания", "Вакансия", "Зарплата", "Ссылка"], tablefmt="pretty"))

        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска: ").strip().lower()
            data = db_manager.get_vacancies_with_keyword(keyword)
            if data:
                print(f"\nВакансии по ключевому слову '{keyword}':")
                print(tabulate(data, headers=["Компания", "Вакансия", "Зарплата", "Ссылка"], tablefmt="pretty"))
            else:
                print(f"\nВакансии по ключевому слову '{keyword}' не найдены.")

        elif choice == '0':
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт из меню.")
