import json

from config import config
from src.utils import (create_database)
from src.hh_api import HeadHunter


if __name__ == '__main__':
    params = config()
    create_database('hh_database', params)

