import requests
import random
import traceback

from requests.exceptions import ConnectionError
from config import Config
from utils.type_hints import LocationArray

"""
TODO:
    1- Caching.
    2- Fault tolerance at the level of OSM instances (so keep trying another instances till you reach a result)
"""


class OSM:
    def __init__(
        self,
        version="v1",
        profile="driving",
        with_time=True,
        with_distance=False,
        skip_waypoints=True,
        time_scale_factor=1,
        api_url=None,
        osm_instances_urls=None,
        load_balance=False,
    ) -> None:
        self.version = version
        self.profile = profile
        self.with_time = with_time
        self.with_distance = with_distance
        self.skip_waypoints = skip_waypoints
        self.time_scale_factor = time_scale_factor
        self.api_url = self._get_api_url(api_url)
        self.osm_instances_urls = self.__get_osm_instances_urls(osm_instances_urls)
        self.load_balance = load_balance
        self.osm_session = requests.Session()

    def osm_table_service_url(self, url: str) -> str:
        params = f"table/{self.version}/{self.profile}/"
        full_url = url if url[-1] == "/" else url + "/"
        return full_url + params

    def _get_api_url(self, value: str) -> str:
        if value:
            if not isinstance(value, str):
                raise Exception("'api_url' should be an str")

            api_url = value
        else:
            api_url = Config.config("OSRM_URL")
        return self.osm_table_service_url(api_url)

    def __get_osm_instances_urls(self, value: list[str]) -> list[str]:
        if value:
            if not isinstance(value, list):
                raise Exception(
                    "'osm_instances_urls' should be a list of OSM instances urls"
                )
            urls = value
        else:
            OSM_CONFIG = Config.config("OSM_CONFIG")
            urls = (
                OSM_CONFIG["OSRM_URLS"]
                if OSM_CONFIG
                and "OSRM_URLS" in OSM_CONFIG
                and isinstance(OSM_CONFIG["OSRM_URLS"], list)
                else []
            )

        return [self.osm_table_service_url(url) for url in urls]

    def __get_current_osm_url(self) -> str:
        if self.load_balance and self.osm_instances_urls:
            osm_url = self.osm_instances_urls[
                random.randint(0, len(self.osm_instances_urls) - 1)
            ]
        else:
            osm_url = self.api_url
        return osm_url

    def osm_matrix(
        self, locations: LocationArray, srcs: list[int], dests: list[int]
    ) -> dict:
        osm_url = self.__get_current_osm_url()

        points = ""
        for idx, loc in enumerate(locations):
            if idx != len(locations) - 1:
                points += loc[1] + "," + loc[0] + ";"
            else:
                points += loc[1] + "," + loc[0]
        osm_url += points

        # Initialize params
        annotations = ""

        if self.with_time:
            annotations += "duration"
        if self.with_distance:
            annotations = annotations + "," + "distance" if annotations else "distance"

        skip_waypoints = self.skip_waypoints

        scale_factor = self.time_scale_factor
        params = {
            "sources": ";".join([str(i) for i in srcs]),
            "destinations": ";".join([str(i) for i in dests]),
            "annotations": annotations,
            "skip_waypoints": "true" if skip_waypoints else "false",
            "scale_factor": scale_factor,
        }

        headers = {"Content-Type": "text/xml; charset=utf-8"}

        try:
            response = self.osm_session.get(osm_url, params=params, headers=headers)
            data = response.json()

            keys = annotations.split(",")

            return {key: data[key + "s"] for key in keys}
        except ConnectionError:  # This osm instance is not working
            traceback.print_exc()
