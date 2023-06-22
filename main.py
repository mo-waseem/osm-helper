import time
from locations import generate_random_locations
from osm_api import osrm_matrix


def test():
    locations = generate_random_locations(
        (30.222676136092296, 31.455316886214952), number=100
    )

    st_time = time.time()
    times = osrm_matrix(
        locations,
        [i for i in range(len(locations)//2)],
        [i for i in range(len(locations)//2, len(locations))],
    )

    #print(times)
    print(time.time()-st_time)
    print(len(times[0][0]), len(times[0]))


test()
