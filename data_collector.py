from repository import advertisement_repository

import parser


def collect_todays_ads(area_coordinates):
    for area, coordinates in area_coordinates.items():
        geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to = coordinates

        print("Getting results")
        ads = parser.get_ads(geo_lat_from, geo_lng_from,
                             geo_lat_to, geo_lng_to)
        print("Result for area " + area + " received")

        # save results to disk
        advertisement_repository.save(ads, area)


area_coordinates_in = {
    "akrwtirh_chaniwn": [35.586164290432315, 24.22181871834033, 35.50051995151323, 24.055793251624152],
    "cholargos": [38.00569499931162, 23.81705586339865, 37.99207158270631, 23.789786511364525]
}

collect_todays_ads(area_coordinates_in)
