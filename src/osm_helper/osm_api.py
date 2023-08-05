import requests
import random

from requests.exceptions import ConnectionError
from config import Config
from utils.type_hints import LocationArray
from utils.redis import Redis
from utils import get_hashed_str


class OSM:
    def __init__(
        self,
        version: str="v1",
        profile: str="driving",
        with_time: bool=True,
        with_distance: bool=False,
        skip_waypoints: bool=True,
        time_scale_factor: int=1,
        api_url: str=None,
        osm_instances_urls: list=None,
        load_balance: bool=False,
        cache_results: bool=False,
        max_api_retries: int=10,
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
        self.cache_results = cache_results
        self.max_api_retries = self.__get_max_api_retries(max_api_retries)

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

    def __get_max_api_retries(self, max_api_retires):
        config_retries = Config.config("OSRM_MAX_API_RETRIES")
        return config_retries if config_retries else max_api_retires
    
    def __get_osm_instances_urls(self, value: list[str]) -> list[str]:
        if value:
            if not isinstance(value, list):
                raise Exception(
                    "'osm_instances_urls' should be a list of OSM instances urls"
                )
            urls = value
        else:
            OSRM_URLS = Config.config("OSRM_URLS")
            urls = OSRM_URLS if isinstance(OSRM_URLS, list) else []

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
        self,
        locations: LocationArray,
        srcs: list[int],
        dests: list[int],
        request_id: str = None,
    ) -> dict:
        if self.cache_results and not request_id:
            raise Exception(
                "When activate 'cache_results' you need to pass 'request_id' to osm_matrix()" # noqa
            )
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

        if self.cache_results:
            redis_key = (
                get_hashed_str(
                    "".join([str(loc) for loc in locations])
                    + params["sources"]
                    + params["destinations"]
                    + params["annotations"]
                    + params["skip_waypoints"]
                    + str(params["scale_factor"])
                )
                + f"_{request_id}"
            )
            data = Redis.get(redis_key)
            if data:
                return data
            
        retries, try_another_osm, osm_urls_number, osm_url_index, success_request = (
            0,
            True,
            len(self.osm_instances_urls) if self.osm_instances_urls else 1,
            0,
            False,
        )
        
        while (
            (retries < self.max_api_retries or try_another_osm) and not success_request
        ):
            try:
                response = self.osm_session.get(osm_url, params=params, headers=headers)
                success_request = True
            except ConnectionError:
                if osm_url_index < osm_urls_number:
                    osm_url = (
                        self.osm_instances_urls[osm_url_index]
                        if self.osm_instances_urls
                        else self.__get_current_osm_url()
                    ) + points
                    osm_url_index += 1
                    if osm_url_index == osm_urls_number:
                        try_another_osm = False
                retries += 1

        if not success_request:
            raise Exception("All of the provided OSRM urls are not working.")
        
        data = response.json()
        keys = annotations.split(",")
        data = {key: data[key + "s"] for key in keys}
        if self.cache_results:
            expire_in = Config.config("REDIS_EXPIRATION_TIME")
            if Config.config("REDIS_ASYNC_CACHE"):
                Redis.acache(redis_key, data, expire_in=expire_in)
            else:
                Redis.cache(redis_key, data, expire_in=expire_in)
        return data
