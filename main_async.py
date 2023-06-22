import time
import multiprocessing

from threading import Thread
from locations import generate_random_locations
from osm_api import osrm_matrix


def fetch(coordinate_batch, i, srcs, result):
    result[i] = osrm_matrix(
        coordinate_batch, srcs, [i for i in range(1, len(coordinate_batch))]
    )


def get_time_matrix(coordinates, srcs, dests, profile="driving", batch_size=50):
    dests_locations = [coord for i, coord in enumerate(coordinates) if i in dests]
    manager = multiprocessing.Manager()
    result = manager.dict()
    processes = []
    batch_size = len(srcs) // (2*16)
    batch_size = batch_size if batch_size else 1
    tasks = []
    for i in range(0, len(srcs), batch_size):
        coordinate_batch = [coordinates[src] for src in srcs[i:i+batch_size]] + dests_locations
        task = Thread(target=fetch, args=(coordinate_batch,
                i,
                srcs[i:i+batch_size],
                result,))
        task.start()
        tasks.append(task)
    for task in tasks:
        task.join()

        # process = multiprocessing.Process(
        #     target=fetch,
        #     args=(
        #         coordinate_batch,
        #         i,
        #         srcs[i:i+batch_size],
        #         result,
        #     ),
        # )
        # processes.append(process)
        # process.start()
    
    # for process in processes:
    #     process.join()

    return result


# Example usage
locations = generate_random_locations(
    (30.222676136092296, 31.455316886214952), number=10
)


st_time = time.time()


times = get_time_matrix(
    locations,
    srcs=[i for i in range(len(locations) // 2)],
    dests=[i for i in range(len(locations) // 2, len(locations))],
)

print(time.time() - st_time)
