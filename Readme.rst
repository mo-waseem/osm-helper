# OSM-HELPER: A fast way to get the ETA (Estimated Time of Arrival)
Do you have multiple python projects for Delivery, Ride-hailing or any logistics service, and each time you need to build the `get_eta` function from scratch ?

This simple package is your right way!

`osm-hepler` is a pretty simple package for making the process of getting eta for a number of locations to be the easiest part in your project (just two lines of code).

The package built on top of  [`OSRM` (Open Source Routing Machine) project](https://project-osrm.org/).

# Features

1- **A default parameters** (that make the performance better) are initialized and they are configurable.

2- **Caching** the results.

3- **Load balancing** between more than one `osrm` instance.

4- **Fault tolerance**: if one of the `osrm` instances is down, it will search for another (this will be done by default in the package). 

## Examples
### Simple Example
```
import time

from locations import generate_random_locations
from osm_api import OSM

# Generate 10 random locations
locations = generate_random_locations(
	("30.222676136092296", "31.455316886214952"), number=10
)

def  default_parameters_example():
	start_time = time.time() # Measring time purpose
	
	# Create a pretty simple OSM instance
	osm_api = OSM()

	# Get the times
	result = osm_api.osm_matrix(
			locations,
			[i for i in  range(len(locations)//2)], # sources indexes
			[i for i in  range(len(locations)//2, len(locations))], # destinations indexes
	)

	elapsed_time = time.time() - start_time
	
	print("Default parameters example elapsed time:", elapsed_time)
	print(result)

default_parameters_example()
```
By running the code, you will get tow things:

1- `elapsed_time`: Elapsed time (calculations time).
2- `result`: Time matrix.

 ### Caching and Load balancing Example
 ```
 def  with_cache_and_load_balance_example():
		start_time = time.time()
	
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
	
with_cache_and_load_balance_example()
```
 
## Configuration

The configuration of this package is done by an .env file and .yaml file like the following (the following files will have the full configs but only `PRIMARY_OSRM_URL` is mandatory)

### .env file
```
YAML_CONFIG_FILE_NAME=YOUR_OSM_HELPER_CONFIG.yaml
```
### YOUR_OSM_HELPER_CONFIG.yaml
```
PRIMARY_OSRM_URL:
	http://router.project-osrm.org

OSRM_URLS: # this in case of multiple osrm instances
	- http://router.project-osrm.org
	- http://localhost:8001 # May be a docker instance

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

You're welcome!
Fork the project and make a pull request I will see it inshallah.
