from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_add_custom_zone_name_cus_zone(self):
        base_dict = {
            'name': "cus_zone",
            'security_type': 'trusted',
        }
        trusted_dict = {"zones": [base_dict]}
        zoneres = zoneobj_api.add_zone_object(**trusted_dict)
        Assertion.assert_equal(zoneres, True, "ERR: Add Zone Failed")
