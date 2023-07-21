import time
from locations import generate_random_locations
from osm_api import OSM


def test():
    locations = generate_random_locations(
        ("30.222676136092296", "31.455316886214952"), number=10
    )

    st_time = time.time()
    osm_api = OSM(load_balance=True, with_distance=True)
    times = osm_api.osm_matrix(
        locations,
        [i for i in range(len(locations)//2)],
        [i for i in range(len(locations)//2, len(locations))],
    )

    #print(times)
    print(time.time()-st_time)
    print(times)


test()
