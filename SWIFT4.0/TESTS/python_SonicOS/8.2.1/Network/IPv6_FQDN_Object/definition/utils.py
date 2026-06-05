import re
import time
from runner.settings import logger


def get_ttl_from_fqdn_ao(output: str):
    if 'TTL' in output:
        getttlvalue = re.search(r'(?<=TTL=)\d+', output, re.I)
        logger.info(f'getttlvalue is:{getttlvalue}')
        if getttlvalue:
            ttlvalue = getttlvalue.group()
            logger.info(f'ttlvalue is:{ttlvalue}')
            return ttlvalue
        else:
            logger.info('resolved ips ares expried')
    else:
        logger.info("there are no resolved in output")
        return ''


def start_capture_and_clear_packets(packet_monitorapi):
    stratres = packet_monitorapi.start_capture()
    logger.info(f'start packet monitor result: {stratres}')
    clearres = packet_monitorapi.clear_packets()
    logger.info(f'clear packet monitor result: {clearres}')


def check_resend_dns_query_and_mark_ttl(packet_monitorapi, **kwargs):
    stopres = packet_monitorapi.stop_capture()
    logger.info(f'stop packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    time.sleep(10)
    logger.info(f'exportres is {exportres}')
    kwargs["pclogin"].send_command('cat /tmp')
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = kwargs["pclogin"].send_command(cmd)
    logger.info(f'********************fitter dns packet result: {pccmdres}')
    if pccmdres:
        dnslist = pccmdres.split("Packet comments")
        checkquerylist = ['User Datagram Protocol', 'Domain Name System (query)',
                          f'{kwargs["domainname"]}: type {kwargs["domaintype"]}, class IN']
        checkresponselist = ['User Datagram Protocol', 'Domain Name System (response)',
                             f'{kwargs["domainname"]}: type {kwargs["domaintype"]}, class IN, addr {kwargs["resolvedip"]}']
        for dnspacket in dnslist:
            checkqueryres = [i in dnspacket for i in checkquerylist]
            if all(checkqueryres):
                for dnspacket_1 in dnslist:
                    checkresponseres = [i in dnspacket_1 for i in checkresponselist]
                    if all(checkresponseres):
                        return all(checkresponseres), dnspacket_1
    else:
        return False, ''


def check_dns_udp_packets(packet_monitorapi, pc_login, domainname, type='mixed'):  # type = A, AAAA ,mixed
    answersmixresipv4list = []
    answersmixresipv6list = []
    stopres = packet_monitorapi.stop_capture()
    time.sleep(10)
    logger.info(f'stop packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    time.sleep(10)
    # logger.info(f'exportres is {exportres}')
    pc_login.send_command('cat /tmp')
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = pc_login.send_command(cmd)
    # logger.info(f'********************fitter dns packet result: {pccmdres}')
    packetslist = pccmdres.split('Packet comments\n')
    filter_ipv4list = ['User Datagram Protocol', 'Domain Name System (response)',
                       f'{domainname}: type A, class IN']
    filter_ipv6list = ['User Datagram Protocol', 'Domain Name System (response)',
                       f'{domainname}: type AAAA, class IN']
    if type == 'A':
        for eachpacket in packetslist:
            checkres = [i in eachpacket for i in filter_ipv4list]
            if all(checkres):
                logger.info(eachpacket)
                # answersipv4res = re.findall(r'(?<=class IN, addr )\d+\.\d+\.\d+\.\d+', eachpacket, re.I | re.S | re.M)
                answersipv4res =  re.findall(rf'(?<={domainname}: type A, class IN, addr )\d+\.\d+\.\d+\.\d+', eachpacket, re.I | re.S | re.M)
                logger.info(f'answersipv4res is:{answersipv4res}')
                if answersipv4res:
                    return answersipv4res
        return []

    if type == 'AAAA':
        for eachpacket in packetslist:
            checkres = [i in eachpacket for i in filter_ipv6list]
            if all(checkres):
                logger.info(eachpacket)
                answersipv6res = re.findall(r'(?<=class IN, addr )\d+\:\d+\::[A-Za-z0-9]+', eachpacket,
                                            re.I | re.S | re.M)
                logger.info(f'answersipv6res is:{answersipv6res}')
                if answersipv6res:
                    return answersipv6res
        return []

    if type == 'mixed':
        for eachpacket in packetslist:
            checkipv4res = [i in eachpacket for i in filter_ipv4list]
            checkipv6res = [i in eachpacket for i in filter_ipv6list]
            if all(checkipv4res):
                logger.info(eachpacket)
                # answersipv4res = re.findall(r'(?<=class IN, addr )\d+\.\d+\.\d+\.\d+', eachpacket, re.I | re.S | re.M)
                answersipv4res =  re.findall(rf'(?<={domainname}: type A, class IN, addr )\d+\.\d+\.\d+\.\d+', eachpacket, re.I | re.S | re.M)
                logger.info(f'answersipv4res is:{answersipv4res}')
                if answersipv4res:
                    answersmixresipv4list = answersipv4res
            if all(checkipv6res):
                logger.info(eachpacket)
                answersipv6res = re.findall(r'(?<=class IN, addr )\d+\:\d+\::[A-Za-z0-9]+', eachpacket,
                                            re.I | re.S | re.M)
                logger.info(f'answersipv6res is:{answersipv6res}')
                if answersipv6res:
                    answersmixresipv6list = answersipv6res
        return answersmixresipv4list, answersmixresipv6list
