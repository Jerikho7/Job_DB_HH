from config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunter
from src.user_interface import user_interface
from src.utils import create_database, insert_data_to_database


def main():
    params = config()
    # Название базы данных
    database_name = 'hh_database'
    # Создание базы данных
    create_database(database_name, params)

    # Получение данных о работодателях и вакансиях с hh.ru
    hh = HeadHunter()
    employers_data = hh.get_employers_with_vacancies()

    # Загрузка данных в базу данных
    insert_data_to_database(employers_data, database_name, params)

    # Работа с базой данных через менеджер
    db_manager = DBManager(database_name, params)

    # Запуск пользовательского интерфейса
    user_interface(db_manager)

if __name__ == '__main__':
     main()
