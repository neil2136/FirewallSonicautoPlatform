import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from modules.API.diag import DiagApi

ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

dns_setting ={
    'dnsProxySupportFragment' : '',# '' or 'on'
    'dns_pry_cache_lifetime': '10',
    'dns_svr_fail_times': '10',
    'dnsOverTCP_enable': '',  #'0' means only udp, '1' means UDP and TCP
    'excludeVPNtraffic': '', #'' or 'on'
}
dns = DiagApi(fw)
dns.dns_proxy_setting(**dns_setting)