from model.advertisement import Advertisement
from string import Template
from bs4 import BeautifulSoup
from typing import List
from parsers import page_parser

import requests
import parsers.page_parser as page_parser


def get_search_coordinates_url(geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to, page=None):
    # geo location parameters
    geo_lat_from_param = 'geo_lat_from=$geo_lat_from'
    geo_lng_from_param = 'geo_lng_from=$geo_lng_from'
    geo_lat_to_param = 'geo_lat_to=$geo_lat_to'
    geo_lng_to_param = 'geo_lng_to=$geo_lng_to'

    # this could be rent, buy etc.
    transaction_name_param = 'transaction_name=buy'
    item_type_param = 'item_type=re_residence'

    parameters = [transaction_name_param, item_type_param, geo_lat_from_param,
                  geo_lng_from_param, geo_lat_to_param, geo_lng_to_param]

    template_url = "https://www.xe.gr/property/results?" + '&'.join(parameters)

    search_url = Template(template_url).substitute(geo_lat_from=geo_lat_from,
                                                   geo_lng_from=geo_lng_from, geo_lat_to=geo_lat_to, geo_lng_to=geo_lng_to)

    if page:
        return search_url + "&page=" + str(page)
    return search_url


def get_search_geo_place_url(geo_place_id, page=None):
    # this could be rent, buy etc.
    transaction_name_param = 'transaction_name=buy'
    item_type_param = 'item_type=re_residence'

    geo_place_id_param = 'geo_place_ids[]=$geo_place_id'

    parameters = [transaction_name_param, item_type_param, geo_place_id_param]

    template_url = "https://www.xe.gr/property/results?" + '&'.join(parameters)

    search_url = Template(template_url).substitute(
        geo_place_id=geo_place_id)

    if page:
        return search_url + "&page=" + str(page)
    return search_url


test_coordinate_url = 'https://www.xe.gr/property/results?transaction_name=buy&item_type=re_residence&geo_lat_from=38.03708590052267&geo_lng_from=23.810839727050507&geo_lat_to=37.9445886039919&geo_lng_to=23.665838954078765'
assert test_coordinate_url == get_search_coordinates_url(
    38.03708590052267, 23.810839727050507, 37.9445886039919, 23.665838954078765)

test_geo_place_url = 'https://www.xe.gr/property/results?transaction_name=buy&item_type=re_residence&geo_place_ids[]=ChIJ45GSSTSYoRQRMHu54iy9AAQ'
assert test_geo_place_url == get_search_geo_place_url(
    "ChIJ45GSSTSYoRQRMHu54iy9AAQ")

# https://www.xe.gr/property/results?transaction_name=buy&item_type=re_residence&geo_place_ids[]=ChIJ45GSSTSYoRQRMHu54iy9AAQ
# geo_place_ids[]=ChIJ45GSSTSYoRQRMHu54iy9AAQ


def get_coordinates_ads(geo_lat_from: float, geo_lng_from: float, geo_lat_to: float, geo_lng_to: float) -> List[Advertisement]:
    search_url = get_search_coordinates_url(
        geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to)
    response = requests.get(search_url)

    first_page = BeautifulSoup(response.text, "html.parser")

    total_pages = int(first_page.find(
        class_="results-pagination").find_all("li")[-1].a.string)

    all_results = [add for add in page_parser.parse(first_page)]
    for page in range(2, total_pages + 1):
        search_url = get_search_coordinates_url(
            geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to, page)
        response = requests.get(search_url)
        current_page = BeautifulSoup(response.text, "html.parser")

        current_page_results = page_parser.parse(current_page)
        for add in current_page_results:
            all_results.append(add)

    return all_results


def get_geo_places_ads(geo_place_id) -> List[Advertisement]:
    search_url = get_search_geo_place_url(geo_place_id)
    response = requests.get(search_url)

    first_page = BeautifulSoup(response.text, "html.parser")

    total_pages = int(first_page.find(
        class_="results-pagination").find_all("li")[-1].a.string)

    all_results = [add for add in page_parser.parse(first_page)]
    for page in range(2, total_pages + 1):
        search_url = get_search_geo_place_url(geo_place_id, page)
        response = requests.get(search_url)
        current_page = BeautifulSoup(response.text, "html.parser")

        current_page_results = page_parser.parse(current_page)
        for add in current_page_results:
            all_results.append(add)

    return all_results
