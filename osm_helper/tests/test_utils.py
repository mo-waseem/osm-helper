import unittest

from osm_helper.utils import get_hashed_str

class TestUtils(unittest.TestCase):
    def test_hashing_str(self):
        string = "waseem"
        hashed = get_hashed_str(string)
        self.assertEqual(hashed, "ae35e53bbcc20ef95578")