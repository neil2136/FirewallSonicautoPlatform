import re
from runner.settings import Params, logger


def check_show_audit_log_result(cmd: str, output, status=0):
    """
    after configure audit log , input 'show audit log' to check result
    :param output: configure audit log
    :param cmd: the cmd you want to check
    :param status: 1 means enable cmd, 0 means disable cmd.
    :return: True or False
    """
    res = False
    if re.search(cmd, output):
        try:
            cmdstr = 'no ' + cmd
            check = re.search(cmdstr, output)
            if status == 1:
                if not check:
                    res = True
                else:
                    logger.error('Cannot enable {}'.format(cmd))
            elif status == 0:
                if check:
                    res = True
                else:
                    logger.error('Cannot disable {}'.format(cmd))
        except BaseException:
            logger.error('error occurred when input command: show audit log')
    else:
        logger.error(f'{cmd} dont exist in output result.')
    return res


def check_log_automation_result(cmd, output):
    """
    after configure log automation , input 'show log automation' to check result
    :param cmd:  the cmd you want to check
    :param output:
    :return:
    """
    res = False
    check1 = re.search('log automation', output)
    if check1:
        try:
            check2 = re.search(cmd, output)
            if check2:
                res = True
            else:
                logger.error('check {} fail'.format(cmd))
        except BaseException:
            logger.error(
                'error occurred when input command: show log automation')
    else:
        logger.error(f'{cmd} dont exist in output result.')
    return res
