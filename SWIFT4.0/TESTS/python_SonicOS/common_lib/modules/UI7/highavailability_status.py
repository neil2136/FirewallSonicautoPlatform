import re
from modules.UI7.common_require import *

class HighAvailabilityStatus:
    ''' HighAvailabilityStatus '''

    def str_compare(self, compstr, basestr):
        if ' ' not in compstr:
            if re.search(compstr, basestr, re.I):
                return True
        substrs = compstr.split(' ')
        rc = 0
        for item in substrs:
            if re.search(item, basestr, re.I):
                rc = rc + 1
        if rc == len(substrs):
            return True
        return False

    def get_ha_status_to_hash(self):
        self.navigation.navigate_to_ha_status_section()
        stat_str = self.ui_wrapper.get_element('class', 'fw-mgmt-ftr-high-availability-status').text
        pattern = re.compile(r'High Availability\s+\w+', re.I)
        sub_stats = pattern.findall(stat_str)
        stat_items = re.split(pattern, stat_str)
        del stat_items[0]
        stat_dict = {}

        for count in range(0, len(sub_stats)):
            stat_dict.update({sub_stats[count]: {}})
            item = stat_items[count].strip()
            # pprint(stat_dict)
            stat_details = item.split('\n')
            # pprint(stat_details)
            for i in range(0, len(stat_details), 2):
                stat_dict[sub_stats[count]].update({stat_details[i]: stat_details[i + 1]})

        pprint.pprint(stat_dict)
        return stat_dict

    def get_status_detail(self, stat_dict, test_area='all'):
        value = ''
        for key in stat_dict.keys():
            for sub_key in stat_dict[key].keys():
                if self.str_compare(test_area, sub_key):
                    value = stat_dict[key][sub_key]
                    logger.info("Find area " + test_area)
                    return value
        if len(value) == 0:
            logger.error("Didn't find the key word " + test_area + ".")
            return False


    def compare_status(self, expect_stat, real_stat):
        fail_list = []
        for area in expect_stat:
            stat = self.get_status_detail(real_stat, area)
            if type(stat) != str:
                logger.error("Please pass in a more strict test_area")
                Assertion.fail(area + " puzzled.")
            logger.info('Real Status: ' + stat)
            logger.info('Expect Status: ' + expect_stat[area])
            if expect_stat[area].lower() != stat.lower():
                fail_list.append(area)
        Assertion.assert_equal(fail_list, [], ", ".join(fail_list) + " areas compare failed.")