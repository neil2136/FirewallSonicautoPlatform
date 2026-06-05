#!/usr/bin/python
# import os
# import sys
import re
import time
from runner.settings import logger
from definition.settings import logger


def add_nm_and_check_nm_status(networkmonitorapi, **kwargs):
    res = networkmonitorapi.add_network_monitor(**kwargs)
    nm_name = kwargs["network_monitors"][0]["policy"]["ipv4"]["name"]
    checkres = False
    if res:
        nmstatus = networkmonitorapi.get_network_monitor_status_by_name(nm_name)
        logger.info(f'yellow is {nmstatus}')
        if nmstatus:
            if 'yellow' in str(nmstatus):
                for i in range(1, 4):
                    time.sleep(20)
                    logger.info(f'*********start to check nm status for {i} time')
                    nmstatus = networkmonitorapi.get_network_monitor_status_by_name(nm_name)
                    logger.info(f'green is {nmstatus}')
                    if nmstatus['led'] == 'green' and nmstatus['netMonProbeStatus']['probesSent'] >= 4:
                        receivednum1 = nmstatus['netMonProbeStatus']['probesSent']
                        time.sleep(10)
                        nmstatus = networkmonitorapi.get_network_monitor_status_by_name(nm_name)
                        receivednum2 = nmstatus['netMonProbeStatus']['probesSent']
                        logger.info(
                            f'responsesReceived: receivednum1 is:{receivednum1},receivednum2 is:{receivednum2}')
                        if receivednum2 > receivednum1:
                            checkres = True
                            return checkres
                        else:
                            logger.info("response of probe doesn't increase")
                            networkmonitorapi.del_network_monitor(nm_name, version=4)
                            networkmonitorapi.add_network_monitor(**kwargs)
                    else:
                        logger.info("***********nm policy led doesn't turn to green,start to check again")
                        networkmonitorapi.del_network_monitor(nm_name, version=4)
                        networkmonitorapi.add_network_monitor(**kwargs)
                else:
                    logger.info(f'***************finish checking for 3 times')
            else:
                logger.error('new network monitor led is not yellow.')
        else:
            logger.info("this nm policy didn't configured")
    else:
        logger.error("add nm policy failed")
    return checkres
