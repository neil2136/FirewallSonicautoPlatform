import re
from runner.settings import Params, logger


def get_uuid(org, commentname):
    try:
        for block in org.split('exit'):
            if commentname in block:
                uuidstr = re.findall('uuid \S+', block)
                if uuidstr:
                    uuid = uuidstr[0].split('uuid ')[-1]
                    if uuid:
                        return uuid
                else:
                    logger.error(
                        'can not find the uuid name in comment {} block.'.format(
                            commentname))
    except BaseException:
        logger.error('error occurred in find uuid process.')
    return 'fail'


def split_address(address):
    try:
        if "," in address:
            start = address.split(",")[0]
            end = address.split(",")[1]
            logger.info(
                "start_ip is : {}, end_ip/netmask is : {}".format(start, end))
            return start + ' ' + end
        else:
            return address
    except BaseException:
        logger.error('error occurred when split address.')
    return 'fail'
