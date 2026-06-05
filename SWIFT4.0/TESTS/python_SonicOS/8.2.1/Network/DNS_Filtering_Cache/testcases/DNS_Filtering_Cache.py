from definition.settings import *
from definition.utils import *


class TestCombine_Cache(Test):
    uuid = 'NonTC'
    description = 'combine test of DNS Filter Cache'

    def test_00_enable_dns_proxy_cache(self):
        enCache = {
            'dns_cache': True
        }
        rc = dnspxy_api.config_dnsproxy(**enCache)
        Assertion.assert_equal(rc, True, "ERR: Disable DNS Proxy Cache failed !! ")

    def test_01_add_dns_rule(self):
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed !! ")

    @repeat_method(6)
    def test_02_do_dig_query_to_get_category(self):
        res = dnspxy_api.flush_caches('ipv4')
        logger.info(f'Flush DNS Proxy ipv4 cache......{res}')
        rc = query_category_result(domain_list=categorized_domains.keys())
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: do_dig_query_to_get_category failed !! ")
        
    def test_03_check_dns_proxy_cache(self):
        # cache json: {"domain_name": "adult.com", "type": "Dynamic", "ip_address": "66.254.114.236", "time_to_live": "Expired", "category": "Pornography"}
        rc = True
        logger.info(f"{' Show DNS Proxy Cache Report ':.^70}")
        caches = dnspxy_api.show_dns_proxy_caches_report()
        logger.info(f"{' Check DNS Proxy Cache Category ':.^70}")
        if caches:
            for domain in categorized_domains.keys():
                logger.info(f"{f' Check Proxy Cache for <{domain}> ':.^70}")
                target_c = categorized_domains[domain]
                for cache in caches:
                    category = cache.get('category')
                    res = category == target_c and cache.get('domain_name') == domain
                    if res:
                        if category == ' ':
                            target_c = 'No Category'
                        cache_result_dict[target_c] = res
                        break
                else:
                    res = False
                    logger.info(f'Need to re-test category <{target_c}> !!! ')
                    re_test_category_list.append(target_c)                    
                logger.info(f' {res}\n')
        else:
            logger.error(f'Failed to get DNS Proxy cache report !!!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check dns proxy cache failed!!!")
        
    def test_04_re_test_error_category(self):
        logger.info('Error category list: ' + str(re_test_category_list))
        for re_test_category in re_test_category_list:
            dnspxy_api.flush_caches('ipv4')
            query_category_result(domain_list=categorized_domains_backup[re_test_category])
            logger.info(f"{' Check DNS Proxy Cache Category ':.^70}")
            cache = dnspxy_api.show_dns_proxy_caches_report()
            if cache:
                cache_result_dict[re_test_category] = re_test_category in json.dumps(cache)
                logger.info(f' {cache_result_dict[re_test_category]}\n')
            else:
                logger.error(f'Failed to get DNS Proxy cache report !!!')
        Assertion.assert_equal(all(cache_result_dict.values()), True, "ERR: combination test failed!!!")

    def test_05_delete_added_dns_rule(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete_dns_rule failed")


# Expected: check Adult category domain cache result
class TestSettings_1520984(Test):
    uuid = "SOSAIOT-TC-51509"
    # uuid = 'F64A4F8E-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520984', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520984')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Adult'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Gaming category domain cache result
class TestSettings_1520985(Test):
    uuid = "SOSAIOT-TC-51510"
    # uuid = 'F64AD418-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520985', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520985')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Gaming'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Gambling category domain cache result
class TestSettings_1520986(Test):
    uuid = "SOSAIOT-TC-51511"
    # uuid = 'F64B3D86-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520986', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520986')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Gambling'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Malware category domain cache result
class TestSettings_1520987(Test):
    uuid = "SOSAIOT-TC-51512"
    # uuid = 'F64BA582-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520987', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520987')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Malware'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Phishing category domain cache result
class TestSettings_1520988(Test):
    uuid = "SOSAIOT-TC-51513"
    # uuid = 'F64C0C7A-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520988', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520988')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Phishing'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Pornography category domain cache result
class TestSettings_1520989(Test):
    uuid = "SOSAIOT-TC-51514"
    # uuid = 'F64DE4FA-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520989', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520989')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Gaming'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Anonymous Proxies category domain cache result
class TestSettings_1520990(Test):
    uuid = "SOSAIOT-TC-51515"
    # uuid = 'F64E4DAA-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520990', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520990')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Anonymous Proxies'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Social category domain cache result
class TestSettings_1520991(Test):
    uuid = "SOSAIOT-TC-51516"
    # uuid = 'F64EB4B6-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520991', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520991')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Social'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Spyware category domain cache result
class TestSettings_1520992(Test):
    uuid = "SOSAIOT-TC-51517"
    # uuid = 'F64F1BE0-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520992', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520992')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Spyware'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Sports category domain cache result
class TestSettings_1520993(Test):
    uuid = "SOSAIOT-TC-51518"
    # uuid = 'F64F859E-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520993', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520993')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Sports'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Hacking/Warez/P2P category domain cache result
class TestSettings_1520994(Test):
    uuid = "SOSAIOT-TC-51519"
    # uuid = 'F64FECFA-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520994', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520994')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Hacking/Warez/P2P'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Violence category domain cache result
class TestSettings_1520995(Test):
    uuid = "SOSAIOT-TC-51520"
    # uuid = 'F650541A-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520995', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520995')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Violence'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Dating category domain cache result
class TestSettings_1520996(Test):
    uuid = "SOSAIOT-TC-51521"
    # uuid = 'F650CF1C-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520996', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520996')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Dating'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Drugs category domain cache result
class TestSettings_1520997(Test):
    uuid = "SOSAIOT-TC-51522"
    # uuid = 'F65137A4-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520997', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520997')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Drugs'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Alcohol category domain cache result
class TestSettings_1520998(Test):
    uuid = "SOSAIOT-TC-51523"
    # uuid = 'F651A220-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520998', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520998')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Alcohol'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check Discrimination/Hate category domain cache result
class TestSettings_1520999(Test):
    uuid = "SOSAIOT-TC-51524"
    # uuid = 'F652180E-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1520999', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520999')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'Discrimination/Hate'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check No category domain cache result
class TestSettings_1521000(Test):
    uuid = "SOSAIOT-TC-51525"
    # uuid = 'F65281C2-8640-11EB-88E2-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521000', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521000')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cache_result(self):
        category = 'No Category'
        Assertion.assert_equal(cache_result_dict[category], True, f"ERR: check {category} cache result failed")


# Expected: check ipv6 domain cache result
class TestSettings_2045123(Test):
    uuid = "SOSAIOT-TC-51536"
    description = show_testcase_info(TESTPLAN, '2045123', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2045123')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_dns_rule(self):
        rc = dnsRule_api.add_dns_rule(**add_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_rule failed !! ")

    @repeat_method(6)
    def test_02_do_dig_query_to_get_category(self):
        res = dnspxy_api.flush_caches('ipv6')
        logger.info(f'Flush DNS Proxy ipv6 cache......{res}')
        rc = check_dns_query_no_error(domain=ipv6_domain, opt="AAAA")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: do_dig_query_to_get_category failed !! ")
    
    def test_03_check_dns_proxy_cache(self):
        logger.info(f"{' Show DNS Proxy Cache Report ':.^70}")
        caches = dnspxy_api.show_dns_proxy_caches_report(version="ipv6")
        logger.info(f"{' Check DNS Proxy Cache Category ':.^70}")
        if caches:
            logger.info(f"{f' Check Proxy Cache for <{ipv6_domain}> ':.^70}")
            for cache in caches:
                rc = cache.get('category') == ipv6_category and cache.get('domain_name') == ipv6_domain
                if rc:
                    break
            else:
                rc = False                
            logger.info(f' {rc}\n')
        else:
            logger.error(f'Failed to get DNS Proxy cache report !!!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check dns proxy cache failed!!!")

    def test_04_delete_added_dns_rule(self):
        rc = dnsRule_api.del_dns_rule_by_name(add_rule_dict['dns_policies'][0]['name'])
        Assertion.assert_equal(rc, True, "ERR: Delete_dns_rule failed")
