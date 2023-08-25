# OSM-HELPER: A fast way to get the ETA (Estimated Time of Arrival)  🗺️ 🚀
Do you have multiple python projects for Delivery 🛵, Ride-hailing 🚗 or any logistics service, and each time you need to build the `get_eta` function from scratch ?

This simple package is your right way! 🚀🚀

`osm-hepler` is a pretty simple package for making the process of getting eta for a number of locations to be the easiest part in your project (just two lines of code).

The package built on top of  [`OSRM` (Open Source Routing Machine) project](https://project-osrm.org/). :world_map:  
We can assume it as a python wrapper on top of the `table` service api of the `OSRM` project.  

## Installation  

```
pip install osm-helper
```

## Features

1- **A default parameters** (that make the performance better) are initialized and they are configurable.

2- **Caching** the results.

3- **Load balancing** between more than one `osrm` instance.

4- **Fault tolerance**: if one of the `osrm` instances is down, it will search for another (this will be done by default in the package). 

## Examples
### Simple Example
After installing the lib you can test it by the following:  

```python
from osm_helper.osm_api import OSM

def simple_example():
    locations = [
        ("25.22386255613285", "55.28397838209264"),
        ("25.356481138224012", "55.404779909052124"),
    ]

    # Create a pretty simple OSM instance
    osm_api = OSM()

    # Get the times
    result = osm_api.osm_matrix(
        locations,
        [0], # Source location index
        [1], # Destination location index
    )

    return result

print(simple_example())
```
By running the code (you will got the following result, the value may be changed with a small changes depending on the OSRM instance you are using):
```
{'duration': [[1128.8]]}
```

 ### Caching and Load balancing Example

 You need to install redis and set its config in the .yaml config file:
 ```
REDIS_HOST:
  127.0.0.1

REDIS_PORT:
  6379

REDIS_EXPIRATION_TIME: # Optional
  43200 

REDIS_ASYNC_CACHE: # Optional
  False
```

Then you can:  


```python
from osm_helper.locations import generate_random_locations
from osm_helper.osm_api import OSM

# Generate 10 random locations
locations = generate_random_locations(
    ("30.222676136092296", "31.455316886214952"), number=10
)

# Create an OSM instance
osm_api = OSM(load_balance=True, cache_results=True, with_distance=True)

# Get the times
result = osm_api.osm_matrix(
			locations,
			[i for i in  range(len(locations)//2)],
			[i for i in  range(len(locations)//2, len(locations))],
			request_id="123"
		)

print(result)
```
 ## OSM Class parameters
 | Name | Default | Explaination |
 |------|---------|--------------|
 |with_time|bool: True|-|
 |with_distance|bool: False|If True, you will get a distance matrix in addition to the time matrix in the result|
 |skip_waypoints|bool: True|This will skip waypoints from the response of osrm api, so you will see a performance enhancement by this|
 |time_scale_factor|int: 1|Scale the resulted times by this scalar|
 |api_url|str: Comes from `PRIMARY_OSRM_URL` config. value|This is the api url of the osrm instance|
 |osm_instances_urls|list: Comes from `OSRM_URLS` config. value|This is a list of osrm urls|
 |load_balance|bool: False|If True, to be not useless we need to set `osm_instances_urls`, so the package will request from a random instance|
 |cache_results|bool: False|If True, you need to pass `request_id` to the `osm_api.osm_matrix` so the key in the redis will be a mix between the info of the function parameters and this `request_id`|
 |max_api_retries|int: 10|If the instance is down, so we will try this number of times before return the result|  
 
## Configuration

The configuration of this package is done by an .env file and .yaml file like the following (the following files will have the full configs but only `PRIMARY_OSRM_URL` is mandatory)

### .env file (Optional and the default name of `YAML_CONFIG_FILE_NAME` will be `osm_helper_config.yaml`)
```
YAML_CONFIG_FILE_NAME=YOUR_OSM_HELPER_CONFIG.yaml
```
### YOUR_OSM_HELPER_CONFIG.yaml
| Name                 | Default   | Explaination |
| -------------------- | ------- |-------  |
| PRIMARY_OSRM_URL     | http://router.project-osrm.org         | OSRM url, the default value is the public instance of OSRM.         |       
| [Optional] OSRM_URLS               |  None       | OSRM Instances         |
| [Optional] OSRM_MAX_API_RETRIES | 10 | If the instance is down, so we will try `OSRM_MAX_API_RETRIES` times before return the result |
| [Optional] REDIS_HOST                     | None        | Redis host url         |
| [Optional] REDIS_PORT                    | None        | Redis port        |
| [Optional] REDIS_EXPIRATION_TIME                    |  INFINITY       | Redis records timeout (in seconds)         |
| [Optional] REDIS_ASYNC_CACHE                   | False        | If True, the caching process will be done in async way (To maximize the performance of getting ETA)          |


## Contribution

**You're welcome!**  
Fork the project and make a pull request I will see it inshallah.
