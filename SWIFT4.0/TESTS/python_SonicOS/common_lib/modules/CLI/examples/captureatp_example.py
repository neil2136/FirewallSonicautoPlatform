import sys
#sys.path.append(os.environ['SONICOS_HOME']+'/6.5.4/python_lib')
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
import modules.CLI.captureatp
from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

cap = modules.CLI.captureatp.CaptureATPCli(fw)

#rc = cap.show_capatp()
#print(rc)
#rc = cap.show_capatp_stat()
#print(rc)
rc = cap.enable_capatp(False)   ### Bool para, default is True. False for disable CaptureATP
print(rc)

#cap_dict = {
#    'file-size': 'restrict',               ### 'default' | 'restrict'
#    'file-size-restrict': 1000,            ### <0..4294967295>
#    'file-type-yes': ['exe', 'archives'],  ### archives | exe | office | officex | pdf
#    'file-type-no': ['office', 'pdf'],     ### archives | exe | office | officex | pdf
#    'ex-md5-yes': ['11223344556677889900aabbccddeeff'],  ### md5 entry
#    'ex-md5-no': ['11223344556677889900aabbccddeeff'],   ### md5 entry
#    'ex-addr-action': True,        ### Bool
#    'ex-addr-type': 'ipv6',        ### ipv6 | host | network | range | fqdn | group | mac | name
#    'ex-addr-value': '',             ### for host, fqdn, group, mac, name
#    'ex-addr-ip1': '1.1.1.1',      ### for network (network) and range (start IP)
#    'ex-addr-ip2': '1.1.1.10',     ### for network (mask) and range (end IP)
#    'ex-addr-ipv6': 'network',     ### for ipv6, value: host | network | range | fqdn | group | mac | name
#    'ex-addr-ipv6-value': '',      ### for ipv6 -> host, fqdn, group, mac, name
#    'ex-addr-ipv6-ip1': 'fec0::',  ### for ipv6 -> network (network) and range (start IP)
#    'ex-addr-ipv6-ip2': 64,        ### for ipv6 -> network (mask) and range (end IP)
#}
#rc = cap.conf_capatp(**cap_dict)
#print(rc)

#custom_dict = {
#    'await-verdict': False,             ### Bool
#    #### Only work when await-verdict is False
#    'ex-file-yes': ['exe', 'office'],   ### archives | exe | office | officex | pdf
#    'ex-file-no': ['archives', 'pdf'],  ### archives | exe | office | officex | pdf
#    'ex-addr-action': True,             ### Bool
#    'ex-addr-type': 'ipv6',      ### ipv6 | host | network | range | fqdn | group | mac | name
#    'ex-addr-value': '',         ### for host, fqdn, group, mac, name
#    'ex-addr-ip1': '1.1.1.1',    ### for network (network) and range (start IP)
#    'ex-addr-ip2': '1.1.1.10',   ### for network (mask) and range (end IP)
#    'ex-addr-ipv6': 'range',     ### for ipv6, value: host | network | range | fqdn | group | mac | name
#    'ex-addr-ipv6-value': '',    ### for ipv6 -> host, fqdn, group, mac, name
#    'ex-addr-ipv6-ip1': 'fec0::',      ### for ipv6 -> network (network) and range (start IP)
#    'ex-addr-ipv6-ip2': 'fec0::0001',  ### for ipv6 -> network (mask) and range (end IP)
#}
#rc = cap.conf_custom_behav(**custom_dict)
#print(rc)
