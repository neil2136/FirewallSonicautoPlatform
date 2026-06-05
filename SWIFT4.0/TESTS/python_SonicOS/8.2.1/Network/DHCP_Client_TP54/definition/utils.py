import re
from definition.settings import pc2login, logger


def arp_reply_check(resp, sender_ip_address, target_ip_address):
    packets = resp.split('Packet number: ')
    senderipaddress = f"Sender IP Address: {sender_ip_address}"
    targetipaddress = f"Target IP Address: {target_ip_address}"
    arptype = f"ARP Response"
    packetinfo = f"Consumed"
    for packet in packets:
        if arptype in packet:
            if senderipaddress in packet:
                if targetipaddress in packet:
                    if packetinfo in packet:
                        return True, packet
    return False, False

def dhcp_request_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    header = f"UDP Packet Header"
    for packet in packets:
        if header in packet:
            if srcip in packet:
                if dstip in packet:
                    return True, packet
    return False, False

def icmp_request_check(resp, src_ip, dst_ip, dst_interface):
    packets = resp.split('Packet number: ')
    packetinfo = f"out:{dst_interface}, Forwarded"
    icmptype = 'ICMP Type = 8'
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    for packet in packets:
        if icmptype in packet:
            if srcip in packet and dstip in packet:
                if packetinfo in packet:
                    return True, packet
    return False, False

def config_dhcp_lease_time_on_pc2(deftime, maxtime):
    dhcpconfpath = "/etc/dhcp/dhcpd.conf"
    output = pc2login.send_command(f'cat {dhcpconfpath}')
    logger.info(f'get dhcpd conf result: {output}')
    if output is None:
        logger.error('can not get dhcpd conf from PC2')
        return False
    curdeftime = re.search('(?<=default-lease-time )\d+', output, re.I)
    curmaxtime = re.search('(?<=max-lease-time )\d+', output, re.I)
    if curdeftime and curmaxtime:
        if deftime == curdeftime.group() and maxtime == curmaxime.group():
            logger.error('input deftime and maxtime are same with current dhcpd configure')
            return False
        else:
            pc2login.send_command(f"sed -i '/default/s@{curdeftime.group()}@{deftime}@' {dhcpconfpath}")
            pc2login.send_command(f"sed -i '/max/s@{curmaxtime.group()}@{maxtime}@' {dhcpconfpath}")
            pc2login.send_command('service dhcpd restart')
            catres = pc2login.send_command(f"cat {dhcpconfpath}")
            logger.info(catres)
            if f"default-lease-time {deftime}" in catres and f"max-lease-time {maxtime}" in catres:
                return True
    else:
        logger.error('can not find default-lease-time and max-lease-time from dhcp.conf')
        return False

def check_dhcp_hostname_on_pc2(hostname):
    output = pc2login.send_command("cat /var/lib/dhcpd/dhcpd.leases | tail -8")
    logger.info(output)
    if f'client-hostname "{hostname}"' in output:
        return True
    return False

# need add to common lib network.ArpApi
# def delete_arp_caches(self):
#     cache_resp = self.fw.api_delete(self.url + "reporting/arp/caches")
#     return cache_resp