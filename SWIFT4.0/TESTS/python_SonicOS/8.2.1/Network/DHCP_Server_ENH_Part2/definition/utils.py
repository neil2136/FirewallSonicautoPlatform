from definition.settings import *


def get_pc_eth_mac(pc, eth):
    out = pc.send_command(f"ifconfig {eth} | grep ether | awk " + "'{print $2}'")
    mac = ''.join(out.strip().split(':'))
    return mac


def pc_renew_dynamic_addr(pc=pc3_login):
    return pc.send_commands(
        ['rm -f /var/lib/dhclient/dhclient.leases; killall dhclient; dhclient -r eth1; dhclient -v eth1'])

