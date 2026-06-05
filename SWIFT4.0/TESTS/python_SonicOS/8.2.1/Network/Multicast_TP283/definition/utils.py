import re, time
from runner.settings import Params, logger
from definition.settings import Parameter, PC1_login, PC2_login


def packet_igmp_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    iptype = 'IP Type: IGMP'
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    for packet in packets:
        if iptype in packet:
            if srcip in packet:
                if dstip in packet:
                    return True, packet
    return False, False


def packet_membership_disable_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    packetinfo = 'in:--, out:X2*, Forwarded'
    iptype = f'IP Type: UDP'
    ips = f'Src=[{src_ip}], Dst=[{dst_ip}]'
    for packet in packets:
        if packetinfo in packet:
            if iptype in packet:
                if ips in packet:
                    return True, packet
    return False, False


def packet_membership_enable_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    packetinfo = 'in:X1*(interface), out:--, DROPPED'
    iptype = f'IP Type: UDP'
    ips = f'Src=[{src_ip}], Dst=[{dst_ip}]'
    for packet in packets:
        if packetinfo in packet:
            if iptype in packet:
                if ips in packet:
                    return True, packet
    return False, False


# run igmp server in async mode from PC1 to PC2
def run_igmp_server(path, asyncfile, runfile, desip):
    logger.info('first: delete running server script process...')
    killcmd = 'ps -ef | grep %s | awk "{print $2}" | xargs kill -9' % runfile
    logger.info(f'pc2 kill cmd: {killcmd}')
    # kill the old process if need
    # killres = PC2_login.send_command(killcmd)
    # logger.info(f'pc2 kill process result: {killres}')
    # time.sleep(5)

    logger.info('start run a ssh to pc2 script in pc1...')
    pc2cmd = f'nohup python3 {path}/{runfile}&'
    pc1cmd = f'python3 {path}/{asyncfile} -ip {desip} -c \"{pc2cmd}\"'
    logger.info(f'pc1 running cmd: {pc1cmd}')
    PC1_login.send_command(pc1cmd)

    logger.info('start check the running result in pc2...')
    grepcmd = 'ps -aux | grep igmpserver'
    logger.info(f'pc2 running cmd: {killcmd}')
    pc1res = PC2_login.send_command(grepcmd)
    logger.info(f'pc2 grep process result: {pc1res}')
    res = True if runfile in pc1res else False
    logger.info('run async process from pc1 to pc2 finished')
    return res
