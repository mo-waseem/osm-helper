import requests
import random
from config import Config


osm_session = requests.Session()
"""
    TODO:
        1- Handle large number of locations.
        2- Handle osm session and read more about sessions in general.

        
"""


def osrm_matrix(locations, srcs, dests):
    OSM_CONFIG = Config.config("OSM_CONFIG")
    urls = (
        OSM_CONFIG["OSRM_URLS"]
        if OSM_CONFIG
        and "OSRM_URLS" in OSM_CONFIG
        and isinstance(OSM_CONFIG["OSRM_URLS"], list)
        else []
    )
    osrm_url = (
        urls[random.randint(0, len(urls) - 1)] if urls else Config.config("OSRM_URL")
    )
    points = ""
    for idx, i in enumerate(locations):
        if idx != len(locations) - 1:
            points += str(i[1]) + "," + str(i[0]) + ";"
        else:
            points += str(i[1]) + "," + str(i[0])
    osrm_url += points

    # Initialize params
    annotations = ""
    osm_config = Config.config("OSM_CONFIG")

    if osm_config.get("WITH_TIME", True):
        annotations += "duration"
    if osm_config.get("WITH_DISTANCE", False):
        annotations = annotations + "," + "distance" if annotations else "distance"

    skip_waypoints = osm_config.get("SKIP_WAYPOINTS", True)

    scale_factor = osm_config.get("TIME_SCALE_FACTOR", 1)
    params = {
        "sources": ";".join([str(i) for i in srcs]),
        "destinations": ";".join([str(i) for i in dests]),
        "annotations": annotations,
        "skip_waypoints": "true" if skip_waypoints else "false",
        "scale_factor": scale_factor,
    }

    headers = {"Content-Type": "text/xml; charset=utf-8"}

    try:
        response = osm_session.get(osrm_url, params=params, headers=headers)
        data = response.json()

        keys = annotations.split(",")

        return [data[key + "s"] for key in keys]
    except Exception as e:
        raise Exception(e)
