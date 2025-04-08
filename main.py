import json

from src.hh_api import HeadHunter


def main():
    hh = HeadHunter()
    data = hh.get_employers_with_vacancies()

    examples = data[:2]

    with open('employers_data.json', 'w', encoding='utf-8') as file:
        json.dump(examples, file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в 'employers_data.json'.")

if __name__ == '__main__':
    main()
