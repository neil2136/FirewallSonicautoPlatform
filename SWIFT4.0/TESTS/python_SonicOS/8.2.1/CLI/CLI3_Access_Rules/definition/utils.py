import re
from runner.settings import Params, logger


def filter_access_rule(customlist, commentname):
    if customlist:
        splitlist = customlist.split('exit')
        if splitlist:
            for split in splitlist:
                if commentname in split:
                    return split
            return 'Error: Can not find the custom comment.'
        else:
            return 'Error: Can not split the custom access rules via exit'
    else:
        return 'Error: Can not search the valid access rules.'


def get_acl_uuid(org, commentname):
    try:
        for ablock in org.split('exit'):
            if commentname in ablock:
                uuidstr = re.findall('uuid \S+', ablock)
                if uuidstr:
                    uuid = uuidstr[0].split('uuid ')[-1]
                    if uuid:
                        return uuid
                else:
                    logger.info(
                        'can not find the uuid name in comment {} block.'.format(
                            commentname))
    except BaseException:
        logger.error('error occurred in find uuid process.')
    return 'fail'