from tabulate import tabulate

from config import config  # твои параметры подключения
from src.db_manager import DBManager
from src.hh_api import HeadHunter  # твой класс для сбора данных
from src.utils import create_database, insert_data_to_database  # функции для работы с БД


def main():
    params = config()
    # Название базы данных
    database_name = 'hh_database'
    db_manager = DBManager(database_name, params)

    def print_table(data, headers):
        print(tabulate(data, headers=headers, tablefmt='fancy_grid', stralign='center', numalign='center'))

    print("\nКомпании и количество вакансий:")
    companies = db_manager.get_companies_and_vacancies_count()
    print_table(companies, ["Компания", "Количество вакансий"])

    print("\nВсе вакансии:")
    vacancies = db_manager.get_all_vacancies()
    print_table(vacancies, ["Компания", "Вакансия", "Зарплата", "Ссылка"])

    print("\nСредняя зарплата по вакансиям:")
    avg_salary = db_manager.get_avg_salary()
    print(f"{avg_salary:.2f} ₽")

    print("\nВакансии с зарплатой выше средней:")
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print_table(higher_salary_vacancies, ["Компания", "Вакансия", "Зарплата", "Ссылка"])

    print("\nВакансии по ключевому слову 'Python':")
    keyword_vacancies = db_manager.get_vacancies_with_keyword('Python')
    print_table(keyword_vacancies, ["Компания", "Вакансия", "Зарплата", "Ссылка"])

    db_manager.close()



if __name__ == '__main__':
    main()
