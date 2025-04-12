import psycopg2
from typing import List, Tuple


class DBManager:
    """
    Класс для работы с базой данных вакансий и работодателей.
    """

    def __init__(self, database_name: str, params: dict):
        """
        Инициализация соединения с базой данных.
        :param database_name: Название базы данных.
        :param params: Параметры подключения.
        """
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список кортежей (название компании, количество вакансий).
        """
        self.cur.execute(
            """
            SELECT employer_name, COUNT(vacancies.employer_id)
            FROM employers
            INNER JOIN vacancies USING (employer_id)
            GROUP BY employer_name
            ORDER BY COUNT DESC
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        """
        Получает список всех вакансий с указанием:
        названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: Список кортежей (название компании, название вакансии, зарплата, ссылка на вакансию).
        """
        self.cur.execute(
            """
            SELECT e.employer_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            WHERE v.salary IS NOT NULL AND v.salary != 0
            ORDER BY v.salary DESC
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по всем вакансиям.
        :return: Средняя зарплата.
        """
        self.cur.execute(
            """
            SELECT AVG(salary) FROM vacancies
            WHERE salary IS NOT NULL AND salary != 0
            """
        )
        avg_salary = self.cur.fetchone()[0]
        return round(avg_salary, 2) if avg_salary else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        """
        Получает список вакансий с зарплатой выше средней.
        :return: Список кортежей (название компании, название вакансии, зарплата, ссылка на вакансию).
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute(
            """
            SELECT e.employer_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            WHERE v.salary > %s
            ORDER BY v.salary DESC
            """,
            (avg_salary,)
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, str]]:
        """
        Получает список вакансий, в названии которых содержится переданное ключевое слово.
        :param keyword: Ключевое слово для поиска в названии вакансии.
        :return: Список кортежей (название компании, название вакансии, зарплата, ссылка на вакансию).
        """
        self.cur.execute(
            """
            SELECT e.employer_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            WHERE LOWER(v.vacancy_name) LIKE %s
            """,
            (f'%{keyword.lower()}%',)
        )
        return self.cur.fetchall()

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.cur.close()
        self.conn.close()
