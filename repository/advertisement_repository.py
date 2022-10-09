from model.advertisement import Advertisement
from typing import List

import os
import datetime
import pickle


def create_path_for_today():
    today_path = get_todays_path()
    if not os.path.exists(today_path):
        os.makedirs(today_path)


def get_todays_path():
    today_date = datetime.date.today().strftime("%m_%d_%y")
    return './data/' + today_date


def get_area_file_name(area):
    return get_todays_path() + '/' + area + '.pickle'


def save(ads: List[Advertisement], area: str):
    area_file_name = get_area_file_name(area)
    if not os.path.exists(area_file_name):
        create_path_for_today()
        with open(area_file_name, 'wb+') as f:
            pickle.dump(ads, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(area_file_name, 'rb+') as f:
            ads = pickle.load(f)
            for ad in ads:
                print(ad.area)
