import sys
import os
sys.path.append(os.environ['SONICOS_HOME']+'/6.5.4/python_lib')
#sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
import modules.CLI.system
from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

#### Status ####################################
stat = modules.CLI.system.StatusCli(fw)

#out = stat.show_status()
#print(out)


#### LicenseCli ################################
license = modules.CLI.system.LicenseCli(fw)

#out = license.show_license_status()
#print(out)

#out = license.show_license()
#print(out)

#(rc, out) = license.sync_online()
#print([rc, out])


#### AdminCli ##################################
admin = modules.CLI.system.AdminCli(fw)

#out = admin.show_admin_setting()
#print(out)

#admin_info = {
#    'name': 'admin',
#    'old_password': 'password',
#    'new_password': 'Admin@123456789',
#    'inactive-time': 10,               ### <1..9999>
#    'preempt-action': 'logout',        ### logout | goto-non-config
#    'one-time-pass': False
#############################################################################
####  The following configuration are dangrous, if you don't know         ###
####  what it is or how it works, please don't specify!                   ###
####  'name'            - admin name admin, can be changed but not empty  ###
####  'one-time-pass'   - bool                                            ###
####  'unbind-totp-key' - True or just not pass in                        ###
#############################################################################
#}
#rc = admin.config_admin(**admin_info)
#print(rc)

#rc = admin.dashboard_starting()     ### Bool, default is True
#print(rc)
#rc = admin.audit_logging()          ### Bool, default is True
#print(rc)
#rc = admin.firewall_name('C0EAE4E8E88C')  ### 'no' or 'disable' or False for no firewall name
#print(rc)
#rc = admin.firewall_domain()        ### False for no firewall domain, default is False
#print(rc)

#admin_gms = {
#    'mode': False,                  ### 'existing-tunnel' | 'https' | 'ipsec-tunnel' | False
#    #### Only for 'mode' is not False
#    'host-name': '1.1.1.1',         ### Must
#    'nat-device': '2.2.2.2',        ### an IP address | other string for no nat device
#    'heartbeat-status-only': True,  ### Bool
#    'syslog-server-port': 24,
#    #### Only for ipsec-tunnel mode
#    'auth-key': 'bd5a1354f5a5a8e19f8c6ae4fb897002',  ### HEX String must 32 bit for MD5
#    'encr-type': 'des-md5',
#    'encr-key': '9f8c6ae4fb897002'  ### HEX String must 16 bit for MD5
#}
#rc = admin.gms_manage(**admin_gms)
#print(rc)

#rc = admin.http_port(80)
#print(rc)
#rc = admin.https_port(443)
#print(rc)
#rc = admin.idle_logout_time(500)
#print(rc)
#rc = admin.inter_admin_msg(5)       ### False or interval value
#print(rc)
#rc = admin.ipv6(False)              ### Bool, default is True
#print(rc)

#res = admin.language_override()     ### Bool, default is True. Restart feature
#print(res)

#rc = admin.multiple_admin(False)    ### Bool, default is True
#print(rc)

#rc = admin.outband_manage(False)    ### Bool, default is True. Restart feature
#print(rc)

#rc = admin.override_down_url('n', False)  ### para1: ac/n/ndr/nv  para2: url or False
#print(rc)

### Need change password first if set complexity or length
#password_dict = {
#    'aging': 30,                    ### Bool or aging time
#    'complexity': False,            ### False or 'alpha-and-numeric-and-symbols'/'alpha-and-numeric'
#    'enforce-diff': False,          ### Bool
#    'minimum-length': 8,            ### False or min length
#    'constraint': True,             ### Bool
#    'constraint_list': ['full-admins', 'local-users'],  ### builtin-admin | full-admins |
#                                                        ### limited-admins | local-users | guest-admins
#    'uniqueness': 5                 ### Bool or value (0..32)
#}
#rc = admin.config_password(**password_dict)
#print(rc)

#api_dict = {
#    'sonicos-api': False,               ### Bool
#    'basic': True,                      ### Bool
#    'chap': False,                      ### Bool
#    'digest': False,                    ### Bool
#    'hold-password': False,             ### Bool
#    'integrity-protection': 'allowed',  ### Bool or 'allowed'/'enforced'
#    'max-nonce': 123,                   ### Value
#    'md5-digest': True,                 ### Bool
#    'public-key': True,                 ### Bool
#    'rsa-key-size': 512,                ### Value
#    'rsa-padding-type': 'pkcsv15',      ### 'pkcsv15' | 'pkcsv20oaep'
#    'session-security': True,           ### Bool
#    'sha256-digest': True,              ### Bool
#    'two-factor-bearer-token': False,   ### Bool
#}
#rc = admin.sonicos_api(**api_dict)
#print(rc)

#rc = admin.tls_above()  ### Bool, default True
#print(rc)
#rc = admin.user_lockout('failures-duration', 10)  ### para1: False or failures-rate |
#print(rc)                                         ### failures-duration | lockout-duration
#                                                  ### para2: rate

#web_manage = {
#    'allow-http': True,         ### Bool
#    'client_cert_check': False, ### Bool
#    'default-table-size': 20,   ### Value
#    'refresh-interval': 10,     ### Value
#    'cert-common-name': False,  ### Bool
#    'cert-type': 'name',        ### 'name' | 'use-self-signed'
#    'cert-name': '',            ### cert name, default 'Use Selfsigned Certificate'
#    'tooltip': False,           ### Bool
#    #### Only use when tooltip is True
#    'form-delay': 500,
#    'button-delay': 500,
#    'text-delay': 500,
#}
#rc = admin.web_manage(**web_manage)
#print(rc)

#rc = admin.wireless_ctl_mode('wireless-controller')  ### non-wireless-controller | normal-firewall |
#print(rc)                                                ### wireless-controller. Restart feature
#rc = admin.wireless_lan()  ### Bool, default is True
#print(rc)


#### SNMPCli ##################################
snmp = modules.CLI.system.SNMPCli(fw)

#rc = snmp.show_snmp_setting()
#print(rc)
#rc = snmp.disable_snmp()
#print(rc)

#snmp_dict = {
#    'asset-number': False,           ### False or value
#    'get-community-name': 'test 1',  ### False or value
#    'system-contact': 'test',        ### False or value
#    'system-location': 'test' ,      ### False or value
#    'system-name': 'test',           ### False or value
#    'trap-community-name': 'test',   ### False or value
#    'host1': '1.1.1.1',              ### False or value
#    'host2': '1.1.1.2',              ### False or value
#    'host3': '1.1.1.3',              ### False or value
#    'host4': '1.1.1.4',              ### False or value
#}
#rc = snmp.conf_snmp(**snmp_dict)
#print(rc)

#rc = snmp.conf_group('test')  ### para1: group name  para2: True for add, False for remove, default is True
#print(rc)
#rc = snmp.conf_view('CorpSNMPViewList', '1.3.6.1.2.1.32')  ### para1: view name  para2: view oid
#print(rc)

#access_dict = {
#    'name': 'test',                                   ### Must str
#    'edit_name': 'test1',                             ### Want to change name to edit_name
#    'master-group': 'test',                           ### Value
#    'read-view': 'CorpSNMPViewList',                  ### Value, must
#    'security-level' : 'authentication-and-privacy',  ### 'authentication-only' | 'authentication-and-privacy'
#}
#rc = snmp.conf_access(**access_dict)
#print(rc)

#snmp3_dict = {
#    'engine-id': '80002225030017C5696969',
#    'incr_sub_pri': False,  ### Bool
#    'mandatory': False      ### Bool
#}
#rc = snmp.conf_snmp3(**snmp3_dict)
#print(rc)

#user_dict = {
#    'remove': False,          ### Bool
#    'user-name': 'test2',
#    'edit-name': 'test3',
#    'group': 'test',
#    'security-level': 'authentication-and-privacy',  ### 'authentication-only' |
#                                                     ### 'authentication-and-privacy' or False
#    #### Only work when security-level is string
#    'auth-method': 'md5',     ### 'md5' | 'sha1'
#    'auth-key': 'password',
#    'en-method': 'aes',       ### aes | des
#    'en-key': 'password'
#}
#rc = snmp.conf_user(**user_dict)
#print(rc)


#### CertificateCli ###########################
cert = modules.CLI.system.CertificateCli(fw)

#rc = cert.show_cert('Amazon Root CA 1')
#print(rc)
#rc = cert.show_certs('build-in')  ### para1: build-in | imported | empty, para2; with-expired
#print(rc)

#### NEED VERIFY ####
#import_dict = {
#    'type': '',                   ### ca-cert | cert-key-pair | crl | signed-cert
#    'protocol': 'scp',            ### scp | ftp
#    'server': '192.168.168.169',
#    'file': 'root/file',
#    'user': 'root',               ### ftp or scp server user
#    'passwd': 'password',         ### ftp or scp server password
#    'ca-name': 'test',
#    'ca_passwd': 'password',
#    'cert-key-pair': 'Corp VPN Cert',
#    'signed-cert' : 'Corp VPN Cert',
#}
#rc = cert.import_cert(**import_dict)

#req_dict = {
#    'alias': 'test',
#    'alt-domain': 'sonicwall.com',
#    'alt-mail': 'auto_email@sonicwall.com',
#    'alt-ipv4': '1.1.1.1',
#    'dis_elm1_country': 'china',             ### At least one dis_elm value
#    'dis_elm2_department': 'Auto',
#    'key-size': 1024,                        ### 1024 | 1536 | 2048 | 256 | 384 | 4096 | 521 
#    'key-type': 'rsa',                       ### ecdsa | rsa
#    'sig-auth': 'md5',                       ### md5 | sha-1 | sha-256 | sha-384 | sha-512
#}
#rc = cert.gen_request(**req_dict)
#print(rc)

#scep_dict = {
#    'ca-url': 'http://scep.mydomain.local',  ### must
#    'sign_req': 'test',                      ### must
#    'passwd': 'password',
#    'max-time': 10,
#    'polling-interval': 10,
#    'request-count': 2,
#}
#rc = cert.conf_scep(**scep_dict)
#print(rc)

#rc = cert.del_cert()  ### cert name | all, default is all
#print(rc)


#### TimeCli ##################################
time = modules.CLI.system.TimeCli(fw)

#rc = time.show_time()
#print(rc)

#time_dict = {
#    'daylight-savings': True,       ### Bool
#    'international-format': False,  ### Bool
#    'only-custom-ntp': False,       ### Bool
#    'universal': True,              ### Bool
#    'use-ntp': True,                ### Bool
#    'time-zone': 'china,philippines',
#    'ntp-update-interval': 10,      ### Value <5..100080>
#    'ntp-server': '1.1.1.1',
#    'ntp_auth': 'md5'               ### md5 | no-auth | empty
#    'trust-key-no': 10,             ### default 10
#    'key-number': 20,               ### default 20
#    'password': 'password'          ### default password
#}
#rc = time.conf_time(**time_dict)
#print(rc)

#rc = time.disable_ntp_svr()  ### ntp server name can be passed in, default is all
#print(rc)


#### ScheduleCli ##############################
schedule = modules.CLI.system.ScheduleCli(fw)

#rc = schedule.show_schedule('Work Hours')  ### para1: all | schedule name like 'Work Hours'
#print(rc)                                  ### para2: pending-config | with-pending-config | empty

#schedule_dict = {
#    'name': 'test1',
#    'edit-name': 'test2',
#    'ocr-mode': 'recurring',    ### mixed | once | recurring. Must
#    'event-start-time': '2019:06:30:00:00',
#    'event-end-time': '2019:06:30:00:01',
#    'rec-time': '12:00 18:00 mon tue wed thu fri'
#}
#rc = schedule.conf_schedule(**schedule_dict)
#print(rc)

#rc = schedule.rem_schedule('test1')
#print(rc)

#rc = schedule.rem_all_schedule()
#print(rc)


#### SettingCli ###############################
setting = modules.CLI.system.SettingCli(fw)

#rc = setting.show_firmware()
#print(rc)

#### NEED VERIFY
#expt_dict = {
#    'period': 'current',         ### current | pending
#    'mode': 'exp',               ### cli | exp, pending only cli
#    'protocol': 'scp',           ### scp | ftp
#    'passwd': 'password',
#    'server': '192.168.168.169',
#    'user': 'root'
#}
#rc = setting.export_setting(**expt_dict)
#print(rc)

#### NEED VERIFY
#import_dict = {
#    'protocol': 'scp',           ### scp | ftp
#    'passwd': 'password',
#    'server': '192.168.168.169',
#    'user': 'root',
#    'file': 'root/setting.sig'
#}
#rc = setting.import_firmware(**import_dict)
#print(rc)

#rc = setting.boot_firmware('current', 'factory-default')  ### para1: current | system-backup
#print(rc)                                                 ### para2: factory-default | empty

#firmware_dict = {
#    'auto': False,              ### Bool
#    'auto_action': 'download',  ### download | update
#    'diagnostics': False,       ### Bool
#}
#rc = setting.conf_firmware(**firmware_dict)
#print(rc)

#rc = setting.backup_firmware()
#print(rc)

#rc = setting.restore()
#print(rc)


#### PacketmonitorCli #########################
pack_mon = modules.CLI.system.PacketmonitorCli(fw)

#rc = pack_mon.show_pack_mon()
#print(rc)

#rc = pack_mon.show_packet('statistics')  ### all | 1,2... | statistics
#print(rc)

#### NEED VERIFY ####
#cap_expt = {
#    'server': '192.168.168.169',
#    'format': 'app-data',         ### app-data | html | libpcap | pcapng | text
#    'protocol': 'scp',            ### scp | ftp
#    'user': 'root',
#    'passwd': 'password'
#}
#rc = pack_mon.export_capture(**cap_expt)
#print(rc)

#cap_info = {
#    'bytes-to-capture': 1520,
#    'dis_bidirectional': True,          ### Bool
#    'dis_dest_ips': '1.1.1.1,2.2.2.2',  ### False or value
#    'dis_dest_ports': '23,25',          ### False or value
#    'dis_ether_types': 'ip',            ### False or value
#    'dis_ifaces': False,                ### False or value like 'X1,X2'
#    'dis_ip_types': False,              ### False or value
#    'dis_src_ips': False,               ### False or value
#    'dis_src_ports': False,             ### False or value
#    'dis_stat': True,                   ### Bool
#    'dis_stat_mode': 'dropped',         ### consumed | dropped | forwarded | generated
#    'ex_encr_gms': True,                ### Bool
#    'ex_in_traffic': True,              ### Bool
#    'ex_in_traf_mode': 'ha',            ### ha | sonicpoint
#    'ex_mgmt': True,                    ### Bool
#    'ex_mgmt_mode': 'ssh',              ### http | snmp | ssh
#    'ex_syslog': True,                  ### Bool
#    'ex_slog_mode': 'syslog-servers',   ### gms-server | syslog-servers
#    'ftp-auto': False,                  ### Bool
#    'ftp-dir': False,                   ### False or value
#    'ftp-html': True,                   ### Bool
#    'ftp-login': False,                 ### False or value
#    'ftp-pass': False,                  ### False or value
#    'ftp-pcapng': False,                ### Bool
#    'ftp-server': '192.168.168.169',    ### False or value
#    'log-to-ftp': True,                 ### True or not pass in
#    'mir-fd-if': False,                 ### False or UTM port
#    'mir-iface': False,                 ### False or UTM port
#    'mir-ip': '1.1.1.1',                ### False or value
#    'mir-max-rate': 100,                ### <100..10000000>
#    'mir-only-ip': True,                ### Bool
#    'mir-rev-ip': False,                ### False or value
#    'mir-cap-buff': True,               ### Bool
#    'monitor': 'all',                   ### all | default
#    'mf-fw-rule': True,                 ### Bool
#    'mf-bidirectional': False,          ### Bool
#    'mf-dest-ips': False,               ### False or value
#    'mf-dest-ports': False,             ### False or value
#    'mf-ether-types': False,            ### False or value
#    'mf-fw-gen': True,                  ### Bool
#    'mf-ifaces': 'X1,X2',               ### False or value
#    'mf-ip-types': False,               ### False or value
#    'mf-src-ips': False,                ### False or value
#    'mf-src-ports': False,              ### False or value
#    'mf_inmed': True,                   ### Bool
#    'mf_inmed_mode': 'ldap-over-tls',   ### fragmented | intermediate-packets | iphelper |
#                                        ### ipsec | ldap-over-tls | multicast |
#                                        ### reassembled | remote-mirrored |
#                                        ### restore-ports-ssl | ssl | sso-agent
#    'mf_stat': True,                    ### Bool
#    'mf_stat_mode': 'forwarded',        ### consumed | dropped | forwarded
#}
#rc = pack_mon.conf_capture(**cap_info)
#print(rc)

#rc = pack_mon.start_capture()
#print(rc)
#rc = pack_mon.stop_capture()
#print(rc)
#rc = pack_mon.start_mirror()
#print(rc)
#rc = pack_mon.stop_capture()
#print(rc)
#rc = pack_mon.wrap_buffer()
#print(rc)


#### PacketreplayCli ##########################
#pack_replay = modules.CLI.system.PacketreplayCli(fw)
#### No function

#### DiagnosticsCli ###########################
diag = modules.CLI.system.DiagnosticsCli(fw)

#rc = diag.show_tsr()
#print(rc)

#### NEED VERIFY ####
#rc = diag.export_tsr('192.168.168.169', 'scp', 'root', 'password')
#print(rc)

#rc = diag.ping('13.11.0.1', 'X1')  ### para1: host, para2: UTM port X1 | MGMT, para3: 1|0 ipv6
#print(rc)
#rc = diag.traceroute('13.11.0.1')  ### para1: host, para2: UTM port X1 | MGMT, para3: 1|0 ipv6
#print(rc)
#rc = diag.nslookup('www.baidu.com', 1, '8.8.8.8')  ### para1: domain, para2: 1|0 ipv6, para3: dns server
#print(rc)
#rc = diag.rbl_lookup('1.1.1.1', 'www.baidu.com', '10.102.1.50')  ### para1: ip, para2: domain, para3: dns
#print(rc)
#rc = diag.network_path('192.168.168.169')
#print(rc)
#rc = diag.reverse_lookup('192.168.168.169', 1, '8.8.8.8') ### para1: ip, para2: 1|0 ipv6, para3: dns server
#print(rc)
#rc = diag.geo_botnet_lookup('192.168.168.169')
#print(rc)
#rc = diag.mxlookup('www.baidu.com')  ### para1: host, para2: port
#print(rc)
#rc = diag.pmtu_discovery('192.168.168.169')  ### para1: host, para2: utm port
#print(rc)

#tsr_dict = {
#    'arp-cache': True,
#    'atp-cache': True,
#    'debug-info': False,
#    'dhcp-bindings': False,
#    'dns-proxy-cache': True,
#    'extra-routing': False,
#    'geo-ip-cache': False,
#    'ike-info': True,
#    'ip-stack-info': True,
#    'secure-backup': False,       ### Bool or interval value
#    'send-raw-flow-data': False,
#    'sonicpointn': False,
#    'vpn-keys': True,
#    'ipv6': True,
#    'ipv6-pro': 'dhcp',           ### dhcp | ndp
#    'user': False,
#    'user-mode': 'detail'         ### current | detail | inactive
#}
#rc = diag.conf_tsr(**tsr_dict)
#print(rc)


#### RestartCli ###############################
restart = modules.CLI.system.RestartCli(fw)

#rc = restart.restart('cancel')  ### default is restart right now, 'cancel' for remove restart plan
#print(rc)                       ### '2019:06:30:23:30:59' | '123 hours' | '10 minutes' | '5 seconds'


#### LegalinforCli ############################
#legal = modules.CLI.system.LegalinforCli(fw)
#### No function
