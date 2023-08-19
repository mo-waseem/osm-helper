# OSM-HELPER: A fast way to get the ETA (Estimated Time of Arrival)  :car::motorcycle::world_map::rocket:
Do you have multiple python projects for Delivery :motorcycle:, Ride-hailing :car: or any logistics service, and each time you need to build the `get_eta` function from scratch ?

This simple package is your right way! :rocket::rocket:

`osm-hepler` is a pretty simple package for making the process of getting eta for a number of locations to be the easiest part in your project (just two lines of code).

The package built on top of  [`OSRM` (Open Source Routing Machine) project](https://project-osrm.org/). :world_map:  
We can assume it as a python wrapper on top of the `table` service api of the `OSRM` project.  

## Installation  

You can find the .whl file in the releases section:

```
pip install osm_helper-0.0.1-py3-none-any.whl
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
from osm_helper.locations import generate_random_locations
from osm_helper.osm_api import OSM

# Generate 10 random locations
locations = generate_random_locations(
    ("30.222676136092296", "31.455316886214952"), number=10
)

# Create a pretty simple OSM instance
osm_api = OSM()

# Get the times
result = osm_api.osm_matrix(
    locations,
    [i for i in range(len(locations)//2)],
    [i for i in range(len(locations)//2, len(locations))],
)

print(result) # Time matrix
```
By running the code:
```
{'duration': [[251, 184, 575.3, 283.1, 472], [207.2, 264.5, 413.5, 121.3, 310.2], [192.5, 417, 439, 277.4, 363.2], [70.4, 271.9, 399.5, 177.8, 296.2], [192.2, 190.5, 486.8, 194.6, 383.5]]}
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

elapsed_time = time.time() - start_time

print("Cache and Load balance enabled example elapsed time:", elapsed_time)
print(result)
```
 
## Configuration

The configuration of this package is done by an .env file and .yaml file like the following (the following files will have the full configs but only `PRIMARY_OSRM_URL` is mandatory)

### .env file (Optional and the default name of `YAML_CONFIG_FILE_NAME` will be `osm_helper_config.yaml`)
```
YAML_CONFIG_FILE_NAME=YOUR_OSM_HELPER_CONFIG.yaml
```
### YOUR_OSM_HELPER_CONFIG.yaml
```yaml
PRIMARY_OSRM_URL: # Mandatory
http://router.project-osrm.org

OSRM_URLS: # OPtional, this in case of multiple osrm instances
- http://router.project-osrm.org
- http://localhost:8001 # May be a docker instance

# Optional

REDIS_HOST:
127.0.0.1
REDIS_PORT:
6379
REDIS_EXPIRATION_TIME:
43200 # in seconds
REDIS_ASYNC_CACHE: # If True, the caching process will be done in async way
True
```

## Contribution

**You're welcome!**  
Fork the project and make a pull request I will see it inshallah.
