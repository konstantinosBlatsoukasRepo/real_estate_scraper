import parser

def collect(area_coordinates):
    for area, coordinates in area_coordinates.items():
        geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to = coordinates
        ads = parser.get_ads(geo_lat_from, geo_lng_from, geo_lat_to, geo_lng_to)



area_coordinates_in = {"akrwtirh_chaniwn": (
    35.586164290432315, 24.22181871834033, 35.50051995151323, 24.055793251624152)}

collect(area_coordinates_in)
