from typing import List
from model.advertisement import Advertisement

def parse(doc: str) -> List[Advertisement]:
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