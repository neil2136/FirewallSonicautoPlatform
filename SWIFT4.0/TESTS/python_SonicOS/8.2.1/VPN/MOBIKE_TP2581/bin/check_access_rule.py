from definition.settings import *


def check_auto_access_rule(src_zone, dst_zone, src_net, dst_net, status):
    logger.info('get access rules')
    resp = Lacrule_obj.get_ipv4_access_rule_given_from_to(srczone=src_zone, destzone=dst_zone)
    rules_list = resp['access_rules']
    rc = False
    for rule in rules_list:
        try:
            if rule['ipv4']['source']['address']['name'] == src_net \
                and rule['ipv4']['destination']['address']['name'] == dst_net \
                and rule['ipv4']['enable'] == status:
                logger.info("{} to {} rule has been auto added and {} now".format(src_zone, dst_zone, status))
                rc = True
                return rc
        except Exception as e: 
            logger.error(repr(e))
    logger.info("{} to {} rule not auto added".format(src_zone, dst_zone))
    pprint.pprint(resp)
    return rc

def check_auto_access_rule_deleted(src_zone, dst_zone, src_net, dst_net):
    logger.info('get access rules')
    resp = Lacrule_obj.get_ipv4_access_rule_given_from_to(srczone=src_zone, destzone=dst_zone)
    rules_list = resp['access_rules']
    rc = True
    for rule in rules_list:
        try:
            if rule['ipv4']['source']['address']['name'] == src_net and \
                rule['ipv4']['destination']['address']['name'] == dst_net:
                logger.info("delete {} to {} rule failed".format(src_zone, dst_zone))
                logger.info("all rules:\n{}".format(resp))
                rc = False
                break
            else:
                rc = True
        except Exception as e: 
            logger.error(repr(e))
    logger.info("delete {} to {} rule passed".format(src_zone, dst_zone))
    pprint.pprint(resp)
    return rc
