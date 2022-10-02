from advertisement import Advertisement
from string import Template
from bs4 import BeautifulSoup
from typing import List

import requests

def get_search_url(geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to, page=None):
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


test_url = 'https://www.xe.gr/property/results?transaction_name=buy&item_type=re_residence&geo_lat_from=38.03708590052267&geo_lng_from=23.810839727050507&geo_lat_to=37.9445886039919&geo_lng_to=23.665838954078765'
assert test_url == get_search_url(
    38.03708590052267, 23.810839727050507, 37.9445886039919, 23.665838954078765)


def get_ads(geo_lat_from: float, geo_lng_from: float, geo_lat_to: float, geo_lng_to: float) -> List[Advertisement]:
    search_url = get_search_url(
        geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to)
    response = requests.get(search_url)

    first_page = BeautifulSoup(response.text, "html.parser")

    total_pages = int(first_page.find(
        class_="results-pagination").find_all("li")[-1].a.string)

    all_results = [add for add in parse_page(first_page)]
    for page in range(2, total_pages + 1):
        search_url = get_search_url(
            geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to, page)
        response = requests.get(search_url)
        current_page = BeautifulSoup(response.text, "html.parser")
        current_page_results = parse_page(current_page)
        for add in current_page_results:
            all_results.append(add)

    return all_results


def parse_page(doc: str) -> List[Advertisement]:
    unparsed_ads = doc.find_all(
        attrs={"class": "common-property-ad-body grid-y align-justify"})
    return [parse_ad(unparsed_ad) for unparsed_ad in unparsed_ads]


def parse_ad(ad_html: str) -> Advertisement:

    id, title, price, price_per_sqm, property_level, total_bedrooms, total_bathrooms, construction_year, area, link, price_updates = "", "", "", "", "", "", "", "", "", "", ""

    id, link = "", ""
    if ad_html.a['href']:
        link = ad_html.a['href']
        id = link.split("/")[6]

    if ad_html.find(class_="common-property-ad-title"):
        title = ad_html.find(
            class_="common-property-ad-title").h3.string.strip()

    if ad_html.find(class_="property-ad-price"):
        price = ad_html.find(class_="property-ad-price").string.strip()

    if ad_html.find(class_="property-ad-price-per-sqm"):
        price_per_sqm = ad_html.find(
            class_="property-ad-price-per-sqm").string.strip()

    if ad_html.find(class_="property-ad-level"):
        property_level = ad_html.find(
            class_="property-ad-level").string.strip()

    if ad_html.find(class_="grid-x property-ad-bedrooms-container"):
        total_bedrooms = ad_html.find(
            class_="grid-x property-ad-bedrooms-container").span.string.strip()

    if ad_html.find(class_="grid-x property-ad-bathrooms-container"):
        total_bathrooms = ad_html.find(
            class_="grid-x property-ad-bathrooms-container").span.string.strip()

    if ad_html.find(class_="grid-x property-ad-construction-year-container"):
        construction_year = ad_html.find(
            class_="grid-x property-ad-construction-year-container").span.string.strip()

    if ad_html.find(class_="common-property-ad-address"):
        area = ad_html.find(class_="common-property-ad-address").string.strip()

    return Advertisement(id, title, price, price_per_sqm, property_level, total_bedrooms, total_bathrooms, construction_year, area, link, price_updates)
