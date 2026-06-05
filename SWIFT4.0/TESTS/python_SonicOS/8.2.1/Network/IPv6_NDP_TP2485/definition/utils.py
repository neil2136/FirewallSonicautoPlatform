#!/usr/bin/python
import os
import sys
import getopt
import re
from definition.settings import Parameter
from runner.settings import Params, logger
import time


def check_one_ndp_cache(ndpapi, ipv6_addr, cache_mode):  # mode = 'STATIC', 'DYNAMIC', 'STALE'
    try:
        output = ndpapi.show_NDP_cache()
        if type(output) == dict:
            if output['ip_address'] == ipv6_addr and output['type'] == cache_mode:
                return True
        else:
            for op in output:
                if op['ip_address'] == Parameter.PC1_ETH0_IPV6 and op['type'] == cache_mode:
                    return True
    except Exception as e:
        logger.error(repr(e))
        return False

