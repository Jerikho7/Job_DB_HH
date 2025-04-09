import requests
import time
from typing import List, Dict, Any


class HeadHunter:
    """
    Класс для взаимодействия с API HeadHunter и получения данных о работодателях и их вакансиях.
    """

    def __init__(self):
        """
        Инициализация параметров для запросов к API HeadHunter.
        """
        self.__url: str = 'https://api.hh.ru/'
        self._headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}
        self._params: Dict[str, Any] = {"per_page": 100, "page": 0, "only_with_salary": True}
        self.employers: List[int] = [9694561, 4219, 5919632, 5667343, 9301808,
                                     774144, 10571093, 198614, 6062708, 78638]

    def get_employers_with_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получает данные о работодателях и их вакансиях с фильтрацией нужных полей.

        :return: Список словарей, содержащих информацию о работодателях и их вакансиях.
        """
        employers_data: List[Dict[str, Any]] = []

        with requests.Session() as session:
            session.headers.update(self._headers)

            for employer_id in self.employers:
                employer_url = f"{self.__url}employers/{employer_id}"
                response = session.get(employer_url)

                if response.status_code == 200:
                    employer = response.json()
                    filtered_employer: Dict[str, Any] = {
                        'id': employer.get('id'),
                        'name': employer.get('name'),
                        'description': employer.get('description'),
                        'area': {'name': employer.get('area', {}).get('name')},
                        'open_vacancies': employer.get('open_vacancies'),
                        'vacancies': []
                    }

                    # Пагинация по вакансиям
                    page = 0
                    while True:
                        params = self._params.copy()
                        params.update({
                            "employer_id": employer_id,
                            "page": page
                        })
                        vacancies_url = f"{self.__url}vacancies"
                        vacancies_response = session.get(vacancies_url, params=params)

                        if vacancies_response.status_code == 200:
                            vacancies_data = vacancies_response.json()
                            vacancies = vacancies_data.get('items', [])

                            # Фильтрация вакансий
                            filtered_vacancies = [
                                {
                                    'id': vacancy.get('id'),
                                    'name': vacancy.get('name'),
                                    'alternate_url': vacancy.get('alternate_url'),
                                    'salary': vacancy.get('salary'),
                                    'published_at': vacancy.get('published_at'),
                                    'area': vacancy.get('area', {}).get('name')
                                }
                                for vacancy in vacancies
                            ]

                            filtered_employer['vacancies'].extend(filtered_vacancies)

                            if page >= vacancies_data.get('pages', 0) - 1:
                                break

                            page += 1
                            time.sleep(0.2)  # пауза между страницами
                        else:
                            print(f"Ошибка при получении вакансий работодателя {employer_id}: "
                                  f"{vacancies_response.status_code}")
                            break

                    employers_data.append(filtered_employer)

                else:
                    print(f"Ошибка при получении данных работодателя {employer_id}: {response.status_code}")

                time.sleep(0.5)  # пауза между работодателями

        return employers_data
