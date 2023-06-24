import requests
import random
from config import Config
from utils.type_hints import LocationArray

"""
    TODO:
        1- Handle large number of locations.
        2- Handle osm session and read more about sessions in general.

        
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
        self.osm_instances_urls = self._get_osm_instances_urls(osm_instances_urls)
        self.load_balance = load_balance
        self.osm_session = requests.Session()

    def set_url_params(self, url):
        params = f"table/{self.version}/{self.profile}/"
        full_url = url if url[-1] == "/" else url + "/"
        return full_url + params

    def _get_api_url(self, value: str) -> str:
        if value:
            if not isinstance(value, str):
                raise Exception("'api_url' should be an str")
            api_url = value
        else:
            api_url = Config.config("OSM_CONFIG")["PRIMARY_OSRM_URL"]
        return self.set_url_params(api_url)

    def _get_osm_instances_urls(self, value: list[str]) -> list[str]:
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

        return [self.set_url_params(url) for url in urls]

    def osrm_matrix(
        self, locations: LocationArray, srcs: list[int], dests: list[int]
    ) -> dict:
        if self.load_balance and self.osm_instances_urls:
            osrm_url = self.osm_instances_urls[
                random.randint(0, len(self.osm_instances_urls) - 1)
            ]
        else:
            osrm_url = self.api_url
        points = ""
        for idx, i in enumerate(locations):
            if idx != len(locations) - 1:
                points += str(i[1]) + "," + str(i[0]) + ";"
            else:
                points += str(i[1]) + "," + str(i[0])
        osrm_url += points

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
            response = self.osm_session.get(osrm_url, params=params, headers=headers)
            data = response.json()

            keys = annotations.split(",")

            return {key: data[key + "s"] for key in keys}
        except Exception as e:
            raise Exception(e)
