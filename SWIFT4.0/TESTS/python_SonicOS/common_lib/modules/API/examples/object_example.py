import sys
from pprint import pprint
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall
from modules.API.object import ApplicationApi
from modules.API.object import SecurityActionProfilesApi
from modules.API.object import WebsitesApi
from modules.API.object import CountryApi
from modules.API.object import ReportingProfilesApi
from modules.API.object import PDFApi


ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
application_obj = ApplicationApi(fw)
securityactionprofiles_obj = SecurityActionProfilesApi(fw)

################# ApplicationApi ##################################
application_json =  {
    "application_groups":[
        {
            "name": "test",
            "application": [
                {
                    "name": "163.com Webmail - HTTP Download Attachment"
                },
            ]
        }
    ]
}
#ret = application_obj.add_application_group(**application_json)
#ret = application_obj.get_application_group()
#ret = application_obj.del_application_group("test")

################# SecurityActionProfilesApi #######################
profile_json = {
    "security_action_profiles": [{
        "name": "New Profile",
        "bandwidth_management": {
            "aggregation_method": "per-policy",
            "usage_tracking": False,
            "egress": {
                "enable": True,
                "bandwidth_object": "Default Action Object BWM Egress High"
            },
            "ingress": {
                "enable": True,
                "bandwidth_object": "Default Action Object BWM Ingress High"
            }
        },
#        "gateway_antivirus": {
#            "enable": True,
#            "password_protected_zip": False,
#            "eicar_detection": False
#        },
#        "threat": {
#            "enable": True,
#            "based_on": "profile",
#            "prevent": {
#                "enable": True,
#                "profile": { "group": "DoS Category Profile" }
#            }
#        },
#        "anti_spyware": {
#            "enable": True,
#            "signature_group": {
#                "high_priority": {
#                    "prevent": True
#                }
#            }
#        },
#        "botnet": {
#            "enable": True,
#            "packet_monitor": True,
#            "log": {
#                "enable": True,
#                "redundancy": 0
#            }
#        },
#        "content_filter": {
#            "enable": True,
#            "action": "block",
#            "block": { "page": {} }
#        },
#        "reporting": { "profile": { "global": True } },
#        "user_actions": {
#            "block_page": { "dropped_connections": True },
#            "block_details": True
#        },
#        "tcp": { "timeout": 30 },
#        "unauthenticated_redirect": True
    }]
}
#out = securityactionprofiles_obj.get_security_action_profiles()
#out = securityactionprofiles_obj.add_security_action_profiles(**profile_json)
#out = securityactionprofiles_obj.get_security_action_profile_name('test')
#out = securityactionprofiles_obj.del_security_action_profile_name('New Profile')
#pprint(out)


website_obj = WebsitesApi(fw)
website_json = {
    "website_objects": [
        {
            "name": "baidu1",
            "domain": "baidu1"
        }
    ]
}


#out = website_obj.get_websites_object()
#out = website_obj.add_websites_object(**website_json)
website_group_json = {
    "website_groups": [
        {
            "name": "baidu_g",
            "website_object": [
                {
                    "name": "baidu"
                }
            ]
        }
    ]
}
#out = website_obj.add_websites_group(**website_group_json)

country_json = {
    "country_groups": [
        {
            "name": "China_g",
            "country": [
                {
                    "name": "China"
                }
            ]
        }
    ]
}
country_obj = CountryApi(fw)
#out = country_obj.add_country_group(**country_json)

out = country_obj.del_country_group("China_g")
pprint("------------------")
pprint(out)
pprint("------------------")

################# ReportingProfilesApi ##################################

reportingprofile_obj = ReportingProfilesApi(fw)

# ouput = reportingprofile_obj.get_reporting_profile()

add_reporting_profile_dict = {
    'profile_name': '9999999',
}
# ouput = reportingprofile_obj.add_reporting_profile(**add_reporting_profile_dict)

profile_name = '9999999'
# ouput = reportingprofile_obj.del_reporting_profile(profile_name)

edit_reporting_profile_dict = {
    'old_profile_name': '55',
    'profile_name': '9999999',
}
# ouput = reportingprofile_obj.edit_reporting_profile(**edit_reporting_profile_dict)


############pdf object part#####
udp= {
    'name': 'udp-pdf',
    'negative': False,
    'family':{'udp':'packet-length'},
    'data-type':{"numeric":{"value":10}},###{'hex':12}
}
udp_edit= {
    'name': 'udp-pdf',
    'name': 'udp-new',
    'negative': True,
    'family':{'udp':'packet-length'},
    'data-type':{"hex":{"value":12}},###{'hex':12}
}
pdf = PDFApi(fw)
rc = pdf.add_pdf_obj(**udp)
rc&= pdf.edit_pdf_obj(**udp)
ret = pdf.show_pdf_obj()
rc &= pdf.del_pdf_obj(name='udp-new')

aogroup_dict = {
            "address_groups": [{
                "ipv4": {
                    "address_group": {
                        "ipv4": [
                            {"name": 'tc43group1'},
                            {"name": 'tc43group2'}
                        ]},
                    "name": 'tc43group3'
                }}]}
# aogroupapi = AddressObjectGroupApi(fw)
# aogroupapi.edit_addressgroup_by_name(name='Test_Net', **aogroup_dict)