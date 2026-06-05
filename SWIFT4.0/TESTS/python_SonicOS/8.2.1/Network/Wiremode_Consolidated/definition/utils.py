from definition.settings import Parameter
from runner.settings import Params, logger
import time


# demo 1: if log event only show once in log monitor
def check_log_events(fw_logs):
    filters = (f'dst_ip\': \'{Parameter.PC1_ETH1_IP_NEW}' and 'Application Firewall Alert' and 'Reset/Drop')
    if type(fw_logs) is list:
        for log in fw_logs:
            logger.info(log['time'])
            if filters in str(log):
                logger.info(f'the march log event in list : {log}')
                return True
    elif type(fw_logs) is dict:
        if filters in str(fw_logs):
            logger.info(f'the march log event in dict : {fw_logs}')
            return True
    else:
        logger.info('fw_logs is not list or dict.')
    return False


# demo 2: if log event show multiple times in different time.
def log_event_filter(log, base_time, log_id):
    time_array = time.strptime(log['time'], '%m/%d/%Y %H:%M:%S')
    if time_array >= base_time:
        logger.info('fw log id time is : {}'.format(log['time']))
        if log_id == 793:
            if (Parameter.PC1_ETH1_IP and 'Application Firewall Alert' and 'Reset/Drop') in str(log):
                logger.info(f'the march log id {log_id} event : {log}')
                return True
        elif log_id == 809:
            if (Parameter.PC1_ETH1_IP and 'Gateway Anti-Virus Alert' and 'blocked') in str(log):
                logger.info(f'the march log id {log_id} event : {log}')
                return True
    return False


def check_log_by_time(fw_time, fw_logs, log_id):
    if type(fw_time) is dict:
        part_time = fw_time['time']['date'].replace(':', '/') + ' ' + fw_time['time']['time']
        print(f'part_time: {part_time}')
        base_time = time.strptime(part_time, '%Y/%m/%d %H:%M:%S')

        logger.info(f'fw system base_time is : {part_time}')
        if type(fw_logs) is list:
            for log in fw_logs:
                if log_event_filter(log, base_time, log_id):
                    logger.info('march log event via filter successful !')
                    return True
        elif type(fw_logs) is dict:
            return log_event_filter(fw_logs, base_time, log_id)

        else:
            logger.info('fw_logs is not list or dict.')
    else:
        logger.info('fw_time is not dict.')
    return False


# need add method to trafficGen.py
def send_commands(self, cmds, backend=False):
    # cmds is list: ['pwd', 'cd /var', 'cd www', 'cd html', 'pwd']
    logger.info(f'cmds list: {cmds}')
    shell_cmds = ''
    for cmd in cmds:
        shell_cmds += cmd + ';'
    logger.info(f'real shell cmds: {shell_cmds}')
    if self.ip.lower() != 'localhost':
        if backend:
            stdin, stdout, stderr = self.ssh.exec_command(shell_cmds + ' 1>&2', get_pty=True)
        else:
            stdin, stdout, stderr = self.ssh.exec_command(shell_cmds)
        result = stdout.read().decode(encoding="utf-8")
        if result:
            logger.info(f'stdout result: {result}')
        else:
            result = stderr.read().decode(encoding="utf-8")
            logger.info(f'stderr result: {result}')
        return result
    else:
        result = subprocess.check_output(shell_cmds, shell=True, stderr=subprocess.STDOUT).decode(encoding="utf-8")
        return result
