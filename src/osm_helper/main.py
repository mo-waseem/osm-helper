import time
from locations import generate_random_locations
from osm_api import OSM

# Generate 10 random locations
locations = generate_random_locations(
    ("30.222676136092296", "31.455316886214952"), number=10
)

def default_parameters_example():
    
    st_time = time.time()
    
    # Create a pretty simple OSM instance
    osm_api = OSM()

    # Get the times
    result = osm_api.osm_matrix(
        locations,
        [i for i in range(len(locations)//2)],
        [i for i in range(len(locations)//2, len(locations))],
    )

    elapsed_time = time.time() - st_time
    print("Default parameters example elapsed time:", elapsed_time)
    print(result)

def with_cache_and_load_balance_example():
    st_time = time.time()
    
    # Create an OSM instance
    osm_api = OSM(load_balance=True, cache_results=True, with_distance=True)

    # Get the times
    result = osm_api.osm_matrix(
        locations,
        [i for i in range(len(locations)//2)],
        [i for i in range(len(locations)//2, len(locations))],
        request_id="123"
    )

    elapsed_time = time.time() - st_time
    print("Cache and Load balance enabled example elapsed time:", elapsed_time)
    print(result)


default_parameters_example()
with_cache_and_load_balance_example()

