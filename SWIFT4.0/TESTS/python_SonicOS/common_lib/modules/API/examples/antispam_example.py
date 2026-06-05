import os,sys
import json
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../'
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.antispam import AntiSpamAPI

ip = '10.5.192.37'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
url='/api/sonicos/anti-spam/settings'


Antispam=AntiSpamAPI(fw)


def test_delete_antispam_using_name():
    url='/api/sonicos/access-rules/ipv4/name/testing'
    response=Antispam.delete_antispam(url)
def test_get_antispam_using_name():
    url='/api/sonicos/anti-spam/settings'
    response=Antispam.get_antispam(url)

def test_put_anti_spam():
    anti_spam={
    'anti_spam': {
        'enable': True,
        'action': {
            'likely_spam': 'store',
            'definite_spam': 'delete',
            'likely_phishing': 'tag',
            'definite_phishing': 'store',
            'likely_virus': 'store',
            'definite_virus': 'delete'
        },
        'service_down': 'allow',
        'junk_box': {
            'down': 'tag-deliver'
        },
        'probe': {
            'interval': 5,
            'timeout': 30
        },
        'success_threshold': 1,
        'failure_threshold': 3,
        'mail_server': {
            'public': '0.0.0.0',
            'private': '0.0.0.0',
            'port': 25
        },
        'destination_mail_address_as_junk_store': True,
        'system_detection': True
    }



    }
    print(json.dumps(anti_spam))
    
    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

def TC003_PUT_Likely_Spam_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': { 
            'likely_spam': 'filtering-off'}}}

    response=Antispam.put_antispam(url=url,**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_spam'] == 'filtering-off':
        print('-----------------------------------------'+'TC003 - PASS')
    else:
        print('-----------------------------------------'+'TC003 - FAil')
def TC004_PUT_Likely_Spam_email_catogory_with_Tag_with_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_spam': 'tag'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_spam'] == 'tag':
        print('-----------------------------------------'+'TC004 - PASS')
    else:
        print('-----------------------------------------'+'TC004 - FAil')    
def TC005_PUT_Likely_Spam_email_catogory_with_Delete_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_spam': 'delete'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_spam'] == 'delete':
        print('-----------------------------------------'+'TC005 - PASS')
    else:
        print('-----------------------------------------'+'TC005 - FAil')
def TC006_PUT_Definite_Spam_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': {
           'definite_spam': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)
    print(response)
    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_spam'] == 'filtering-off':
        print('-----------------------------------------'+'TC006 - PASS')
    else:
        print('-----------------------------------------'+'TC006 - FAil')
def TC007_PUT_Definite_Spam_email_catogory_with_Tag_with_action():
    anti_spam={
    'anti_spam': {
    'action': {
       'definite_spam': 'tag'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_spam'] == 'tag':
        print('-----------------------------------------'+'TC007 - PASS')
    else:
        print('-----------------------------------------'+'TC007 - FAil')
def TC008_PUT_Definite_Spam_email_catogory_with_Store_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_spam': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_spam'] == 'filtering-off':
        print('-----------------------------------------'+'TC008 - PASS')
    else:
        print('-----------------------------------------'+'TC008 - FAil')
def TC009_PUT_Likely_Phishing_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': {
           'likely_phishing': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_phishing'] == 'filtering-off':
        print('-----------------------------------------'+'TC009 - PASS')
    else:
        print('-----------------------------------------'+'TC009 - FAil')
def TC010_PUT_Likely_Phishing_email_catogory_with_store_with_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_phishing': 'store',}}}

    response=Antispam.put_antispam(url=url,**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_phishing'] == 'store':
        print('-----------------------------------------'+'TC010 - PASS')
    else:
        print('-----------------------------------------'+'TC010 - FAil')
def TC011_PUT_Likely_Phishing_email_catogory_with_Delete_with_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_phishing': 'delete'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_phishing'] == 'delete':
        print('-----------------------------------------'+'TC011 - PASS')
    else:
        print('-----------------------------------------'+'TC011 - FAil')
def TC012_PUT_Definite_Phishing_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_phishing': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_phishing'] == 'filtering-off':
        print('-----------------------------------------'+'TC012 - PASS')
    else:
        print('-----------------------------------------'+'TC012 - FAil')
def TC013_PUT_Definite_Phishing_email_catogory_with_Tag_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_phishing': 'tag'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_phishing'] == 'tag':
        print('-----------------------------------------'+'TC013 - PASS')
    else:
        print('-----------------------------------------'+'TC013 - FAil')
def TC014_PUT_Definite_Phishing_email_catogory_with_Delete_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_phishing': 'delete',}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_phishing'] == 'delete':
        print('-----------------------------------------'+'TC014 - PASS')
    else:
        print('-----------------------------------------'+'TC014 - FAil')
def TC015_PUT_Likely_Virus_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_virus': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_virus'] == 'filtering-off':
        print('-----------------------------------------'+'TC015 - PASS')
    else:
        print('-----------------------------------------'+'TC015 - FAil')
def TC016_PUT_Likely_Virus_email_catogory_with_Tag_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_virus': 'tag'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_virus'] == 'tag':
        print('-----------------------------------------'+'TC016 - PASS')
    else:
        print('-----------------------------------------'+'TC016 - FAil')
def TC017_PUT_Likely_Virus_email_catogory_with_Delete_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'likely_virus': 'delete'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['likely_virus'] == 'delete':
        print('-----------------------------------------'+'TC017 - PASS')
    else:
        print('-----------------------------------------'+'TC017 - FAil')
def TC018_PUT_Definite_Virus_email_catogory_with_Filtering_Off_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_virus': 'filtering-off'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_virus'] == 'filtering-off':
        print('-----------------------------------------'+'TC018 - PASS')
    else:
        print('-----------------------------------------'+'TC018 - FAil')
def TC019_PUT_Definite_Virus_email_catogory_with_Tag_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_virus': 'tag'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_virus'] == 'tag':
        print('-----------------------------------------'+'TC019 - PASS')
    else:
        print('-----------------------------------------'+'TC019 - FAil')
def TC020_PUT_Definite_Virus_email_catogory_with_store_action():
    anti_spam={
    'anti_spam': {
        'action': {
            'definite_virus': 'store'}}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['action']['definite_virus'] == 'store':
        print('-----------------------------------------'+'TC020 - PASS')
    else:
        print('-----------------------------------------'+'TC020 - FAil')
def TC021PUT_service_down_with_Reject():
    anti_spam={
    'anti_spam': {
        'service_down': 'reject'}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['service_down'] == 'reject':
        print('-----------------------------------------'+'TC021 - PASS')
    else:
        print('-----------------------------------------'+'TC021 - FAil')
def TC022_PUT_junk_box_down_with_Delete():
    anti_spam={
    'anti_spam': {
        'junk_box': {
            'down': 'delete'
        }}}
    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['junk_box']['down'] == 'delete':
        print('-----------------------------------------'+'TC022 - PASS')
    else:
        print('-----------------------------------------'+'TC022 - FAil')
def TC023_PUT_Probe_interval_with_min_max_value():
    anti_spam={
    'anti_spam': {
         'probe': {
            'interval': 1
        }}}
    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)


    anti_spam={
    'anti_spam': {
        'probe': {
            'interval': 60
        }}}
    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['probe']['interval'] == 1 and get_response['anti_spam']['probe']['interval'] == 60 :
        print('-----------------------------------------'+'TC023 - PASS')
    else:
        print('-----------------------------------------'+'TC023 - FAil')
def TC024_PUT_Probe_timeout_with_min_max_value ():
    anti_spam={
    'anti_spam': {
        'probe': {
            'timeout': 29
        }}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)


    anti_spam={
    'anti_spam': {
        'probe': {
            'timeout': 300
        }}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['probe']['timeout'] == 29 and get_response['anti_spam']['probe']['timeout'] == 300 :
        print('-----------------------------------------'+'TC024 - PASS')
    else:
        print('-----------------------------------------'+'TC024 - FAil')
def TC025_PUT_Success_Count_Threshold_with_min_max_value():
    anti_spam={
    'anti_spam': {
    'success_threshold': 10
    }}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['success_threshold'] == 10:
        print('-----------------------------------------'+'TC025 - PASS')
    else:
        print('-----------------------------------------'+'TC025 - FAil')
def TC026_PUT_Failure_Count_Threshold_with_min_max_value():
    anti_spam={
    'anti_spam': {
        'failure_threshold': 1}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)


    anti_spam={
    'anti_spam': {
        'failure_threshold': 10}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['failure_threshold'] == 10:
        print('-----------------------------------------'+'TC026 - PASS')
    else:
        print('-----------------------------------------'+'TC026 - FAil')
def TC027_PUT_Server_Public_Ip_Address():
    anti_spam={
    'anti_spam': {
                'mail_server': {
            'public': '192.168.168.10'
        }}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['mail_server']['public'] == '192.168.168.10':
        print('-----------------------------------------'+'TC027 - PASS')
    else:
        print('-----------------------------------------'+'TC027 - FAil')
def TC028_PUT_Server_Private_IP_Address():
    anti_spam={
    'anti_spam': {
                'mail_server': {
            'private': '192.168.168.11'
        }}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['mail_server']['private'] == '192.168.168.11':
        print('-----------------------------------------'+'TC028 - PASS')
    else:
        print('-----------------------------------------'+'TC028 - FAil')
def TC029_PUT_Inbound_Email_Port():
    anti_spam={
    'anti_spam': {
        'mail_server': {
            'port': 2525
        }}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['mail_server']['port'] == 2525:
        print('-----------------------------------------'+'TC029 - PASS')
    else:
        print('-----------------------------------------'+'TC029 - FAil')
def TC030_PUT_enable_disable_destination_mail_server_as_junk_store():
    anti_spam={
    'anti_spam': {
    'destination_mail_address_as_junk_store': False,
    'junk_store_ip': '192.168.168.13'}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)

    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['destination_mail_address_as_junk_store'] == False:
        print('-----------------------------------------'+'TC030 - PASS')
    else:
        print('-----------------------------------------'+'TC030 - FAil')
def TC031_PUT_enable_disable_system_detection():
    anti_spam={
    'anti_spam': {
    'destination_mail_address_as_junk_store': True}}

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/settings',**anti_spam)
    print(response)
    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['destination_mail_address_as_junk_store']== True:
        print('-----------------------------------------'+'TC031 - PASS')
    else:
        print('-----------------------------------------'+'TC031 - FAil')
def TC033_PUT_Anti_Spam_Allow_List():
    anti_spam={
    'anti_spam': {
        'allow_list': [
            {
                'name': 'X1 IP'
            }
        ]
    }
    }

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/allow-list',**anti_spam)
    print(response)
    get_response=Antispam.get_antispam('/api/sonicos/anti-spam/allow-list')
    print(get_response)
    if get_response['anti_spam']['allow_list'][0]['name'] == 'X1 IP':
        print('-----------------------------------------'+'TC033 - PASS')
    else:
        print('-----------------------------------------'+'TC033 - FAil')
def TC032_GET_Anti_Spam_Allow_List():

    url='/api/sonicos/anti-spam/allow-list'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam('/api/sonicos/anti-spam/allow-list')

    if get_response['anti_spam']['allow_list'][0]['name'] == 'X1 IP':
        print('-----------------------------------------'+'TC032 - PASS')
    else:
        print('-----------------------------------------'+'TC032 - FAil')
def TC034_DELETE_Anti_Spam_Reject_List():
    anti_spam={
    'anti_spam': {
        'reject_list': [
            {
                'name': 'X1 IP'
            }
        ]
    }
    }
    url='/api/sonicos/anti-spam/reject-list'
    response=Antispam.delete_antispam(url,data=anti_spam)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'allow_list' in get_response['anti_spam'].keys():
        print('-----------------------------------------'+'TC032 - FAIL')
    else:
        print('-----------------------------------------'+'TC032 - PASS')
def TC036_PUT_Anti_Spam_Reject_List():
    anti_spam={
    'anti_spam': {
        'reject_list': [
            {
                'name': 'X1 IP'
            }
    ]
    }
    }

    response=Antispam.put_antispam(url='/api/sonicos/anti-spam/reject-list',**anti_spam)
    print(response)
    get_response=Antispam.get_antispam('/api/sonicos/anti-spam/reject-list')
    if get_response['anti_spam']['reject_list'][0]['name'] == 'X1 IP':
        print('-----------------------------------------'+'TC036 - PASS')
    else:
        print('-----------------------------------------'+'TC036 - FAil')
def TC035_GET_Anti_Spam_Reject_List():
    url='/api/sonicos/anti-spam/reject-list'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if get_response['anti_spam']['reject_list'][0]['name'] == 'X1 IP':
        print('-----------------------------------------'+'TC035 - PASS')
    else:
        print('-----------------------------------------'+'TC035 - FAil')
def TC037_DELETE_Anti_Spam_Allow_List():
    anti_spam={
    'anti_spam': {
        'allow_list': [
            {
                'name': 'X1 IP'
            }
        ]
    }
    }

    url='/api/sonicos/anti-spam/allow-list'
    response=Antispam.delete_antispam(url,data=anti_spam)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'allow_list' in get_response['anti_spam'].keys():
        print('-----------------------------------------'+'TC037 - FAIL')
    else:
        print('-----------------------------------------'+'TC037 - PASS')
def TC038_DELETE_Anti_spam_capture():
    url='/api/sonicos/reporting/anti-spam/statistics/capture'
    response=Antispam.delete_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    print(get_response)
def TC039_GET_Anti_spam_capture ():
    url='/api/sonicos/reporting/anti-spam/statistics/capture'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'packet_capture_status' in get_response.keys() :
        print('-----------------------------------------'+'TC039 - PASS')
    else:
        print('-----------------------------------------'+'TC039 - FAil')
def TC040_GET_Anti_spam_statistics_probe():
    url='/api/sonicos/reporting/anti-spam/statistics/probe'
    response=Antispam.get_antispam(url)
    print('sss')
    print(response)
    get_response=Antispam.get_antispam(url)
    print(get_response)
    if 'monitored_server' in get_response.keys() and 'success_count' in get_response.keys() and 'failure_count' in get_response.keys() and 'success_rate' in get_response.keys() :
        print('-----------------------------------------'+'TC040 - PASS')
    else:
        print('-----------------------------------------'+'TC040 - FAil')
def TC041_GET_Anti_spam_statistics_general():
    url='/api/sonicos/reporting/anti-spam/statistics/general'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'number_of_messages_processed' in  get_response.keys() and 'number_of_junk_messages' in  get_response.keys() and 'recorded_since' in  get_response.keys() :
        print('-----------------------------------------'+'TC041 - PASS')
    else:
        print('-----------------------------------------'+'TC041 - FAil')
def TC042_GET_Anti_spam_statistics_threats():
    url='/api/sonicos/reporting/anti-spam/statistics/threats'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'tcp_cookie_syn_flood_validation' in  get_response.keys() and 'static_host_reject_list' in  get_response.keys() and 'grid_ip_reputation_service' in  get_response.keys() and 'likely_spam' in  get_response.keys() and 'definite_spam' in  get_response.keys() and 'likely_phishing' in  get_response.keys() and 'definite_phishing' in  get_response.keys() and 'likely_virus' in  get_response.keys() and 'definite_virus' in  get_response.keys():
        print('-----------------------------------------'+'TC042 - PASS')
    else:
        print('-----------------------------------------'+'TC042 - FAil')
def TC043_GET_Anti_spam_status():
    url='/api/sonicos/reporting/anti-spam/status'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'tcp_cookie_syn_flood_validation' in  get_response.keys() and 'static_host_reject_list' in  get_response.keys() and 'grid_ip_reputation_service' in  get_response.keys() and 'likely_spam' in  get_response.keys() and 'definite_spam' in  get_response.keys() and 'likely_phishing' in  get_response.keys() and 'definite_phishing' in  get_response.keys() and 'likely_virus' in  get_response.keys() and 'definite_virus' in  get_response.keys():
        print('-----------------------------------------'+'TC043 - PASS')
    else:
        print('-----------------------------------------'+'TC043 - FAil')
def TC044_GET_Anti_spam_status_monitoring():
    url='/api/sonicos/reporting/anti-spam/status/service'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'anti_spam_service_expiration_date' in get_response.keys() and 'license_node_count' in get_response.keys() and 'junk_store_version' in get_response.keys()  :
        print('-----------------------------------------'+'TC044 - PASS')
    else:
        print('-----------------------------------------'+'TC044 - FAil')
def TC045_GET_Anti_spam_status_service():
    url='/api/sonicos/reporting/anti-spam/statistics/capture'
    response=Antispam.get_antispam(url)
    print(response)
    get_response=Antispam.get_antispam(url)
    if 'packet_capture_status' in get_response.keys() :
        print('-----------------------------------------'+'TC045 - PASS')
    else:
        print('-----------------------------------------'+'TC045 - FAil')





test_get_antispam_using_name()
test_put_anti_spam()
test_get_antispam_using_name()
TC003_PUT_Likely_Spam_email_catogory_with_Filtering_Off_action()
TC004_PUT_Likely_Spam_email_catogory_with_Tag_with_action()
TC005_PUT_Likely_Spam_email_catogory_with_Delete_action()
TC006_PUT_Definite_Spam_email_catogory_with_Filtering_Off_action()
TC007_PUT_Definite_Spam_email_catogory_with_Tag_with_action()
TC008_PUT_Definite_Spam_email_catogory_with_Store_action()
TC009_PUT_Likely_Phishing_email_catogory_with_Filtering_Off_action()
TC010_PUT_Likely_Phishing_email_catogory_with_store_with_action()
TC011_PUT_Likely_Phishing_email_catogory_with_Delete_with_action()
TC012_PUT_Definite_Phishing_email_catogory_with_Filtering_Off_action()
TC013_PUT_Definite_Phishing_email_catogory_with_Tag_action()
TC014_PUT_Definite_Phishing_email_catogory_with_Delete_action()
TC015_PUT_Likely_Virus_email_catogory_with_Filtering_Off_action()
TC016_PUT_Likely_Virus_email_catogory_with_Tag_action()
TC017_PUT_Likely_Virus_email_catogory_with_Delete_action()
TC018_PUT_Definite_Virus_email_catogory_with_Filtering_Off_action()
TC019_PUT_Definite_Virus_email_catogory_with_Tag_action()
TC020_PUT_Definite_Virus_email_catogory_with_store_action()
TC021PUT_service_down_with_Reject()
TC022_PUT_junk_box_down_with_Delete()
TC023_PUT_Probe_interval_with_min_max_value()
TC024_PUT_Probe_timeout_with_min_max_value ()
TC025_PUT_Success_Count_Threshold_with_min_max_value()
TC026_PUT_Failure_Count_Threshold_with_min_max_value()
TC027_PUT_Server_Public_Ip_Address()
TC028_PUT_Server_Private_IP_Address()
TC029_PUT_Inbound_Email_Port()
TC030_PUT_enable_disable_destination_mail_server_as_junk_store()
TC031_PUT_enable_disable_system_detection()
TC033_PUT_Anti_Spam_Allow_List()
TC032_GET_Anti_Spam_Allow_List()
TC037_DELETE_Anti_Spam_Allow_List()
TC036_PUT_Anti_Spam_Reject_List()
TC035_GET_Anti_Spam_Reject_List()
TC034_DELETE_Anti_Spam_Reject_List()
TC038_DELETE_Anti_spam_capture()
TC039_GET_Anti_spam_capture ()
#TC040_GET_Anti_spam_statistics_probe() this test case have an issue 
TC041_GET_Anti_spam_statistics_general()
TC042_GET_Anti_spam_statistics_threats()
#TC043_GET_Anti_spam_status() this test case is not working
TC044_GET_Anti_spam_status_monitoring()
TC045_GET_Anti_spam_status_service()