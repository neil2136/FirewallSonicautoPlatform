#!/usr/bin/python
# import os
# import sys
import re
import time
from runner.settings import logger
from definition.settings import logger


def get_accessrule_hit_time_in_tsr(tsr_accessrule, accessrule_name):
    hittime = ''
    accessrule_sp = tsr_accessrule.split('Rule ')
    for eachaccessrule in accessrule_sp:
        if f'{accessrule_name}' in eachaccessrule:
            logger.info(f'get accessrule from tsr is {eachaccessrule}')
            hittime = re.search(r'(?<=Time Last Hit:   )\d+/\d+/\d+\s+\d+:\d+:\d+.\d+', eachaccessrule,
                                re.I | re.S).group()
            return hittime
    return hittime