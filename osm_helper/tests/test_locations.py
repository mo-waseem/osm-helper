import unittest

from osm_helper.locations import haversine_distance, generate_random_locations

class TestLocations(unittest.TestCase):
    def test_hav_distance(self):
        """Test haversine_distance()"""
        loc_1 = (30.053073966738072, 31.330581439403396)
        loc_2 = (30.066269330276118, 31.325126427222468)
        distance = haversine_distance(loc_1, loc_2)
        self.assertEqual(round(distance, 2), 1.56)


    def test_generate_random_locations(self):
        locations = generate_random_locations(
            ("30.222676136092296", "31.455316886214952"), number=10
        )
        self.assertEqual(len(locations), 10)

        # All of them are valid
        valid = True
        for loc in locations:
            if (
                not isinstance(loc, tuple)
                or not isinstance(loc[0], str)
                or not isinstance(loc[1], str)
            ):
                valid = False
                break
        self.assertTrue(valid)
