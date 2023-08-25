import unittest

from osm_helper.examples.basic import default_parameters_example


class TestOSMApi(unittest.TestCase):
    def test_with_default_config(self):
        result, _ = default_parameters_example()
        assert 'duration' in result
        
        # since the number of locations in the default example is 10, so the result list is 5x5
        assert len(result["duration"]) == 5

        is_result_length_valid = True
        is_all_zero = True
        for item in result["duration"]:
            if len(item) != 5:
                is_result_length_valid = False
            
            for time in item:
                if time != 0:
                    is_all_zero = False
            
            if not is_result_length_valid and not is_all_zero:
                break

        assert is_result_length_valid
        assert not is_all_zero
