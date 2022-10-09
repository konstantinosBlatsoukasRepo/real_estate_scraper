from repository import advertisement_repository
from parsers import parser


GEO_PLACE_ID_MODE = "GEO_PLACE_ID_MODE"
COORDINATES_MODE = "COORDINATES"


def collect_todays_ads_geo(geo_place_ids):
    for area, geo_place_id in geo_place_ids .items():
        print("Getting results")
        ads = parser.get_geo_places_ads(geo_place_id)
        print("Result for area " + area + " received")

        # save results to disk
        advertisement_repository.save(ads, area)


def collect_todays_ads_coordinates(area_coordinates):
    for area, coordinates in area_coordinates.items():
        geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to = coordinates

        print("Getting results")
        ads = parser.get_coordinates_ads(geo_lat_from, geo_lng_from,
                                         geo_lat_to, geo_lng_to)
        print("Result for area " + area + " received")

        # save results to disk
        advertisement_repository.save(ads, area)


def collect_todays_ads(search_data, mode):
    if mode == COORDINATES_MODE:
        collect_todays_ads_coordinates(search_data)
    elif mode == GEO_PLACE_ID_MODE:
        collect_todays_ads_geo(search_data)


area_coordinates_in = {
    "akrwtirh_chaniwn": [35.586164290432315, 24.22181871834033, 35.50051995151323, 24.055793251624152],
    "cholargos": [38.00569499931162, 23.81705586339865, 37.99207158270631, 23.789786511364525]
}

geo_places_ids_in = {
    "cholargos": "ChIJ45GSSTSYoRQRMHu54iy9AAQ"
}

# collect_todays_ads(area_coordinates_in, COORDINATES_MODE)
collect_todays_ads(geo_places_ids_in, GEO_PLACE_ID_MODE)
