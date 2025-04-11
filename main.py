from config import config  # твои параметры подключения
from src.hh_api import HeadHunter  # твой класс для сбора данных
from src.utils import create_database, insert_data_to_database  # функции для работы с БД


def main():
    params = config()
    # Название базы данных
    database_name = 'hh_database'

    # Создание экземпляра класса HeadHunter
    hh = HeadHunter()

    # Получение данных о работодателях и вакансиях
    print("Получение данных с HeadHunter...")
    employers_data = hh.get_employers_with_vacancies()

    # Создание базы данных и таблиц
    print("Создание базы данных и таблиц...")
    create_database(database_name, params)

    # Загрузка данных в базу данных
    print("Загрузка данных в базу данных...")
    insert_data_to_database(employers_data, database_name, params)

    print("Работа программы завершена успешно!")


if __name__ == '__main__':
    main()
