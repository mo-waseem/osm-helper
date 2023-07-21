import time
import csv
from locations import generate_random_locations
from osm_api import OSM




def test():
    #0.014866113662719727
    # locations = generate_random_locations(
    #     ("30.222676136092296", "31.455316886214952"), number=10
    # )
    locations = []
    with open("locations.csv", "r") as f:
        csvreader = csv.reader(f)
        for i, row in enumerate(csvreader):
            if i == 0:
                continue
            locations.append(row)
    
    # # with open("locations.csv", 'w') as f:
    # #     writer = csv.writer(f)
    # #     writer.writerow(["lat", "lng"])
    # #     writer.writerows(locations)
    
    st_time = time.time()
    osm_api = OSM(load_balance=True, with_distance=True, cache_results=True)
    times = osm_api.osm_matrix(
        locations,
        [i for i in range(len(locations)//2)],
        [i for i in range(len(locations)//2, len(locations))],
        request_id="123"
    )

    # #print(times)
    print(time.time()-st_time)
    print(times)
    # Redis.cache("waseem", "kntar")
    # print(Redis.get("waseem"))


test()
