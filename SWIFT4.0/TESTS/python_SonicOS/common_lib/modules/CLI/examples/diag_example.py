import sys
import os
from pprint import pprint
#sys.path.append(os.environ['SONICOS_HOME']+'/6.5.4/python_lib')
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
import modules.CLI.system
from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

##################### Class DiagCli ###########################
from modules.CLI.diag import DiagCli
diag = DiagCli(fw)

#out = diag.diag_clear('pp-stats')  ### abr-entries | active-utm | cp-stats | hw-stats |  pp-stats
#out = diag.show_abrentries('10.6.0.8') ### ip: can be IPv4 and IPv6
#out = diag.show_activeutm()
#out = diag.show_alerts() ### top: default 0 stands for all alerts, can be > 0
#out = diag.show_bufmemzone()
#out = diag.show_build_info()
#out = diag.show_cores(8) ### core: default 0 stands for all cores, can be 1-9
#out = diag.show_cpstat()
#out = diag.show_cpu()
#out = diag.show_ifdebug('X1') ### iface: can be number, for example 5, then X5 will be passed in
#                              ### can be X0, X1 ... MGMT...
#out = diag.show_dropstats()
#out = diag.show_fpa()
#out = diag.show_hwstat()
#out = diag.show_ipnet('route') ### interfaces | ndp | route | sockets | statistic | tcp-statistic
#out = diag.show_log() ### top: default 0 stands for all logs, can be > 0
#out = diag.show_mempool()
#out = diag.show_mem()
#out = diag.show_memzone(mode='summary', period=1, repeat_mode='5', console=1)
    ### mode: summary | verbose, period: default 0
    ### if period==1, repeat_mode and console can be set
    ### repeat_mode: default '', can be num str like '3' or 'repeat-forever'
    ### console: default 0, can be set 1
#out = diag.show_multicore()
#out = diag.show_netstat()
#out = diag.show_ppstat()
#out = diag.show_process() ### process: default 0 stands for all proceses, can be process str like 'tDDNSS'
#out = diag.show_swport(func='status', iface='3') ### func: counters | status
#                                                 ### iface: can be num str like '3' or 'X0', 'X1' ... 'MGMT'
#out = diag.show_timecount()
#out = diag.show_tracelog() ### period: default '' stands for all logs, can be current | last
#out = diag.show_wdstat()
#out = diag.show_websvr()
#out = diag.show_wmi() ### func: default status, also can be configs

#out = diag.show_advance(func='arp', para='with-pending-config')
#   ### func: default '',
#   ### can be anti-spam | arp | backend | control-plane | dhcp | diagnostics | dial-up | dns
#   ### dns-security | dpi-ssl | encryption | firewall | flow-reporting | geoip-location-service
#   ### high-availability | management | network | pppoe | preference | security-service | ssl-vpn
#   ### user-authentication | voip | vpn | watchdog | wireless | pending-config | with-pending-config
#   ### para: default '', can be pending-config | with-pending-config

#out = diag.diag_lookup(mode='geo-botnet-lookup', simple_para='10.6.0.8')
#para = { 'port': '21' }
#out = diag.diag_lookup(mode='mxlookup', simple_para='192.168.168.169', params=para)
#para = {
#    'ip': '1.1.11.1',
#    'domain': 'www.mysonicwall.com',
#    'dns-server': '10.102.1.50'
#}
#out = diag.diag_lookup(mode='rbl-lookup', params=para)
#    ### mode: geo-botnet-lookup | mxlookup | network-path | rbl-lookup | reverse-lookup | wmi
#    ### simple_para: if mode has only one parameter, add it here
#    ### if more parameters needed, use dict

#out = diag.unconf_diag_advance(para='debug', option='suppress-performance-testing-warning')
#    ### para: can be debug | email-detection | hosted-email-security | icmp | ipv6-ready-enforce
#    ### log-reschedule | remote-assistance | support-windows-messenger | tooltip-no-description | x0-as-mgmt
#    ### option: when pare=='debug', option can be suppress-performance-testing-warning
#    ### suppress-task-dead-warning | suppress-task-lock
#    ### when para=='icmp', option can be drop-exceeded-packet | drop-unreachable-packet

para = {
    'cass_cloud_service_addr': {'static-ip': '10.1.1.1'},
    'check-grid-ip-only': False,
    'disabling-custom-email': False
}
out = diag.conf_diag_adv(func='anti-spam', sub_para=para)
    ### func: anti-spam | arp | backend-server | debug | dhcp | diagnostics | dial-up | dns | dns-security
    ### dpi-ssl | dpi-stateful-firewall-security | email-detection | encryption | firewall | flow-reporting
    ### geoip-location-service | high-availability | hosted-email-security | icmp | ipv6-ready-enforce
    ### log-reschedule | management | network | pppoe | preference | remote-assistance | security-services
    ### sslvpn | stateful-firewall-security | support-windows-messenger | tooltip-no-description
    ### user-authentication | voip | vpn | wan-acceleration | watchdog | wireless | x0-as-mgmt
    ### simple_para: if func has a value, passed by this parameter
    ### sub_para: dict for sub function 

pprint(out)
