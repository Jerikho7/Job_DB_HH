from configparser import ConfigParser
from typing import Dict


def config(filename: str = "database.ini", section: str = "postgresql") -> Dict[str, str]:
    """
    Получает параметры подключения к базе данных из файла конфигурации.

    :param filename: Имя файла конфигурации.
    :param section: Секция конфигурации для базы данных.
    :return: Словарь с параметрами подключения.
    :raises Exception: Если указанная секция не найдена в файле.
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
