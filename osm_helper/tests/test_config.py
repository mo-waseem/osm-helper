import unittest

from osm_helper.config import Config

class TestConfig(unittest.TestCase):
    def test_config(self):
        Config.set("OSRM_URL", "http://localhost:8001")
        self.assertEqual(Config.config("OSRM_URL"), "http://localhost:8001")