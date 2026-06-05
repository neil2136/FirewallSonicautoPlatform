from definition.settings import *


def get_v6_addr(interface='x1'):
    out = if_v6_api.get_interface_address(interface)
    # 匹配IPv6地址直到遇到 / 或 , 或字符串结尾
    match = re.search(r'([0-9a-fA-F:]+?)(?:/|$|,)', out.get('ip_address', ''))
    v6_addr = match.group(1) if match else "::"
    logger.info(f'Got {interface} v6 address is {v6_addr}')
    return v6_addr



def check_traffic_through_v6plus_tunnel_interface(v6_addr):
    pkt_api.clear_packets()
    pkt_api.start_capture()
    out = PC1_login.send_command('ping 12.12.1.100 -c 10')
    if '100% packet loss' in out:
        logger.error('traffic is not pass')
        return False
    else:
        logger.info('traffic is pass, check the packet')
        pkt_api.stop_capture()
        pkts = pkt_api.export_captured_packets()
        pkt_list = pkts.split('Packet number:')
        for pkt in pkt_list[1:]:
            if 'Src=[192.168.168.171]' in pkt and 'Dst=[12.12.1.100]' in pkt:
                logger.info('this is the first packet from LAN client')
                continue
            if 'Src=[192.0.0.2]' in pkt and 'Dst=[12.12.1.100]' in pkt:
                logger.info('this is the second packet which is translate to v6plus IP')
                continue
            if f'Src=[{v6_addr}]' in pkt and f'Dst=[2001:1:2:3::1]' in pkt:
                logger.info('this is the third packet that through v6Plus tunnel')
                return True
        else:
            logger.error('not found any packet through the tunnel.')
            return False
        
    
def create_ipv6_tunnel_interface_on_pc2(remote_v6_addr):
    cmd1 = 'sudo ip link delete t0'
    cmd2 = f'ip link add name t0 type ip6tnl remote {remote_v6_addr} local 2001:1:2:3::1 mode any'
    cmd3 = 'ip link set dev t0 up'
    cmd4 = 'iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE'
    cmd5 = 'ip a add 192.0.0.1/29 dev t0'  
    PC2_login.send_commands([cmd1, cmd2, cmd3, cmd4, cmd5])
