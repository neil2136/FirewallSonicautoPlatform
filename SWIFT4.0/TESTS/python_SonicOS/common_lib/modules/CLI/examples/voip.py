import modules.CLI.voip
from utm import Firewall
'''
Example file for voip lib
'''

fw = Firewall(
    ip = '192.168.168.168',
    user='admin',
    password='password',
    supported_config_mode='cli-ssh',)

voip_obj = modules.CLI.voip.VoIPCli(fw)
voip_show_command = voip_obj.show_voip()
print(voip_show_command)

voip_dict = {
    'consistent-nat': True,
    'sip': True,
    'h323': True,
    'flush-all': True,
}

voip_gen_settings = voip_obj.general_settings(**voip_dict)
print(voip_gen_settings)


sip_dict = {
    'signaling-port': '4560',                #<0..65535> = Integer in the form: D OR 0xHHHH
    'signaling-timeout': '1800',             #<30..100000> = Integer in the form: D OR 0xHHHHHHHH
    'media-timeout': '120',                  #<30..3600> = Integer in the form: D OR 0xHHHH
    'endpoint-block-interval': '3600',       #<10..86400> = Integer in the form: D OR 0xHHHH
    'failed-registration-threshold': '123',  #<1..100> = Integer in the form: D OR 0xHHHH
    'registration-tracking-interval': '300', #<10..86400> = Integer in the form: D OR 0xHHHHHHHH
    'endpoint-registration-anomaly-tracking': True,
    'non-sip-packets': True,
    'b2bua-support': True,
}

voip_sip = voip_obj.sip(**sip_dict)
print(voip_sip)


h323_dict = {
    'inactivity-timeout': '100', # <60..122400> = Integer in the form: D OR 0xHHHHHHHH
    'only-gatekeeper-calls': True,
    'gatekeeper-ip': '192.168.168.168.168', # <IPV4_HOST> = IPV4 Address in the form: a.b.c.d
}

voip_h323 = voip_obj.h323(**h323_dict)
print(voip_h323)