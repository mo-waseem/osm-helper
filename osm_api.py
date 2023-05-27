import requests

from config import OSRM_URL

osm_session = requests.Session()


def osrm_matrix(locations, srcs, dests):
    osrm_url = OSRM_URL
    points = ''
    for idx, i in enumerate(locations):
        if idx != len(locations) - 1:
            points += str(i[1]) + "," + str(i[0]) + ';'
        else:
            points += str(i[1]) + "," + str(i[0])
    osrm_url += points
    params = {
        "sources": ";".join([str(i) for i in srcs]),
        "destinations": ";".join([str(i) for i in dests]),
        "annotations": "distance,duration"
    }
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    try:
        response = osm_session.get(osrm_url, params=params, headers=headers)  # 'Retry-After': '3600'})

        data = response.json()
        return data['distances'], data['durations']
    except Exception as e:
        raise Exception("Error")