import time
from ..locations import generate_random_locations
from ..osm_api import OSM


def default_parameters_example():
    
    st_time = time.time()
    
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

    elapsed_time = time.time() - st_time
    

    return result, elapsed_time

default_parameters_example()