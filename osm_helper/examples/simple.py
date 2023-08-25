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
        [0],
        [1],
    )

    return result

simple_example()
