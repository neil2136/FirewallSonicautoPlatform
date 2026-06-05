# from networkdevice import Firewall
import sys
import os
sys.path.append('/sonicosapiqa/6.5.4/python_lib')
# import modules.API.network
from utm import Firewall
from modules.API.matchobject import MatchObjectApi
ip = '10.5.182.49'

fw = Firewall(ip)
print(fw.__dict__)
url='api/sonicos/match-objects/'
matchonj = MatchObjectApi(fw,url)
def delete_matchobject(name):
    match_object={"object_type":"email-to",
    "name":"email To"}
    get_resp=matchonj.get_matchobject(url)
    if "match_objects" in get_resp.keys():
            list_of_match_obj=get_resp['match_objects']
            for mat_obj in list_of_match_obj:
                if mat_obj["name"]==name:
                    print("in a list")
                    del_url=url+"name"+'/'+name
                    del_response=matchonj.del_matchobject(del_url)
            num_param=1
    elif "match_object" in get_resp.keys():
        match_obj=get_resp['match_object']
        if match_obj["name"]==name:
            num_param=0
            del_url=url+"name"+'/'+name
            del_response=matchonj.del_matchobject(del_url)
            print(del_response)
        else:
            num_param=1
    print(get_resp)

def make_activex():
    match_object = {"object_type":"activex-class-id",
            "name":"activex",
            "match_type":"exact",
            "input_representation":"hexadecimal",
            "content_entry":[{"content_entry": "12345671"},{"content_entry": "1234"}]
            }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)

def delete_activex():
    delete_matchobject("activex")


def make_email_body():
    match_object={"object_type":"email-body",
        "name":"email body2",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "112"},{"content_entry": "1234"}]
        }
    # make_and_delete_email_body()
    print("before get")
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)
def delete_email_body():
        delete_matchobject("email body2")

def make_email_CC():
    match_object={"object_type":"email-cc",
        "name":"email cc",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)
def delete_email_CC():
    delete_matchobject("email cc")

def make_email_from():
    match_object={"object_type":"email-from",
        "name":"email from",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_from():
    delete_matchobject("email from")


def make_email_subject():
    match_object={"object_type":"email-subject",
        "name":"email subject1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    


def delete_email_subject():
    delete_matchobject("email subject1")

def make_email_to():
    match_object={"object_type":"email-to",
        "name":"email To",
        "match_type":"partial",
        # "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_to():
    delete_matchobject("email To")

def make_email_size():
    match_object={"object_type":"email-size",
        "name":"email size",
        "email_size": 20
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_size():
    delete_matchobject("email size")

def make_file_extension():
    match_object={"object_type":"file-extension",
        "name":"file extension",
        "match_type":"exact",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_extension():
    delete_matchobject("file extension")

def make_file_name():
    match_object={"object_type":"file-name",
        "name":"file name1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_name():
    delete_matchobject("file name1")

def make_ftp_command():
    match_object={"object_type":"ftp-command",
        "name":"ftp command",
        "ftp_command": [{"ftp_command": "allocate"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_ftp_command():
        delete_matchobject("ftp command")

def make_http_cookie():
    match_object={"object_type":"http-cookie",
        "name":"http-cookie123",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_cookie():
        delete_matchobject("http-cookie123")   

def make_http_host():
    match_object={"object_type":"http-host",
        "name":"http-host",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_host():
    delete_matchobject("http-host")   

def make_http_referer():
    match_object={"object_type":"http-referer",
        "name":"http referer",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_referer():
    delete_matchobject("http referer")

def make_set_cookie():
    match_object={"object_type":"http-set-cookie",
        "name":"http set cookie",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_set_cookie():
    delete_matchobject("http set cookie")

def make_uri_content():
    match_object={"object_type":"http-uri-content",
        "name":"http uri content1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_uri_content():
    delete_matchobject("http uri content1")

def make_http_url():
    match_object={"object_type":"http-url",
        "name":"http url1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }   
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_url():
    delete_matchobject("http url1")

def make_http_user_agent():
    match_object={"object_type":"http-user-agent",
        "name":"http user agent",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_user_agent():
    delete_matchobject("http user agent")

def make_file_content():
    match_object={"object_type":"file-content",
        "name":"file-content",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_content():
    delete_matchobject("file-content")

def make_file_cmd_val():
    match_object={"object_type":"ftp-command-value",
        "name":"ftp-command-value",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "ftp_command": [{"ftp_command": "account"}],
        "argument": [{"argument": "try2"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_cmd_val():
    delete_matchobject("ftp-command-value")

def make_mime_cust_header():
    match_object={"object_type":"mime-custom-header",
        "name":"mime-custom-header",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "custom_header": "CustomheaderName",
        "content_entry": [{"content_entry": "try3"}]
    }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_mime_cust_header():
    delete_matchobject("mime-custom-header")

def make_http_request_custom_header():
    match_object={"object_type":"http-request-custom-header",
    "name":"http-request-custom-header",
    "match_type":"partial",
    "input_representation":"alphanumeric",
    "negative_matching": False,
    "custom_header": "CustomheaderName",
    "content_entry": [{"content_entry": "try2"}]
    }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_request_custom_header():
    delete_matchobject("http-request-custom-header")

def make_http_response_custom_header():
    match_object={"object_type": "http-response-custom-header",
        "name": "http-response-custom-header",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "custom_header": "CustomheaderName",
         "content_entry": [{"content_entry": "try2"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_response_custom_header():
    delete_matchobject("http-request-custom-header")

def make_web_browser():
    match_object={"object_type": "web-browser",
        "name": "web-browser",
        "match_type":"partial",
        "negative_matching": False,
        "browser": [{"browser": "netscape"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_web_browser():
    delete_matchobject("web-browser")

def make_IPS_signature_category_list():
    match_object={"object_type": "ips-signature-category-list",
        "name": "ips-signature-category-list",
        "ips": {"category": [{"id": 61}]}
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_IPS_signature_category_list():
    delete_matchobject("ips-signature-category-list")

def make_IPS_signature_list():
    match_object={"object_type":"ips-signature-list",
        "name":"ips-signature-list",
        "ips": {"policy": [{"category": {"id": 61},"signature": {"id": 5086}}]}
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_IPS_signature_list():
    delete_matchobject("ips-signature-list")

def make_Application_category_list():
    match_object={"object_type": "application-category-list",
        "name": "application-category-list",
        "category": [{"id": 55}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_category_list():
    delete_matchobject("application-category-list")

def make_application_list():
    match_object={"object_type": "application-list",
        "name": "application-list",
        "application": [{"category": {"id": 55},"app": {"id": 437}}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_list():
    delete_matchobject("application-category-list")

def make_application_signature_list():
    match_object={"object_type": "application-signature-list",
        "name":"application-signature-list",
        "signature": [{"category": {"id": 55},"app": {"id": 437},"sig": {"id": 5600}}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_signature_list():
    delete_matchobject("application-signature-list")

def make_log_email_user():
    match_object={
        "object_type": "log-email-user",
        "name":"log-email-user",
     }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_log_email_user():
    delete_matchobject("log-email-user")

def make_custom_nonen():
    match_object={"object_type":"custom",
        "name":"custom default",
        "match_type":"exact",
        "enable": False,
        "input_representation":"alphanumeric",
        "content_entry": [{"content_entry": "try1"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)   

def delete_custom_nonen():
    delete_matchobject("custom default")

def make_custom_en():
    match_object={"object_type":"custom",
        "name":"custom Enable",
        "match_type":"exact",
        "enable": True,
        "input_representation":"alphanumeric",
        "offset": 2,
        "depth": 1500,
        "min_size": 1,
        "max_size": 1500,
        "content_entry": [{"content_entry": "try1"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)   

def delete_custom_en():  
    delete_matchobject("custom Enable")

def edit_match_object():
    json_put_match_object={
    "match_objects": [
        {
            "name": "http referer",
            "type": "http-referer",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http set cookie",
            "type": "http-set-cookie",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http uri content1",
            "type": "http-uri-content",
            "match_type": "partial",
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http url1",
            "type": "http-url",
            "match_type": "partial",
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http user agent",
            "type": "http-user-agent",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "ftp-command-value",
            "type": "ftp-command-value",
            "match_type": "partial",
            "negative_matching": False,
            "input_representation": "alphanumeric",
            "ftp_command": [
                {
                    "ftp_command": "account"
                }
            ],
            "argument": [
                {
                    "argument": "try2"
                }
            ]
        },
        {
            "name": "http-response-custom-header",
            "type": "http-response-custom-header",
            "match_type": "partial",
            "negative_matching": False,
            "input_representation": "alphanumeric",
            "custom_header": "CustomheaderName",
            "content_entry": [
                {
                    "content_entry": "try2"
                }
            ]
        },
        {
            "name": "application-list",
            "type": "application-list",
            "application": [
                {
                    "category": {
                        "id": 55
                    },
                    "app": {
                        "id": 437
                    }
                }
            ]
        },
        {
            "name": "activex",
            "type": "application-list",
            "application": [
                {
                    "category": {
                        "id": 55
                    },
                    "app": {
                        "id": 437
                    }
                }
            ]
        }
    ]
}
    # url1=url+"name"+"/"+"activex"
    print("url")
    put_match_resp=matchonj.put_match_object(json_put_match_object,url)
# edit_match_object()
# make_email_body()
# make_activex()
delete_activex()
delete_email_body()
# make_email_CC()
# # delete_email_CC()
# make_email_from()
# # # # delete_email_from()
# make_email_subject()
# # # # delete_email_subject()
# make_email_to()
# # # # delete_email_to()
# make_email_size()
# # # # # delete_email_size()
# make_file_extension()
# # # # # delete_file_extension()
# make_file_name()
# make_ftp_command()
# # # # delete_ftp_command()
# make_http_cookie()
# # # # delete_http_cookie()
# make_http_host()
# # # # delete_http_host()
# make_http_host()
# # # delete_http_host()
# make_http_referer()
# # # delete_http_referer()
# make_set_cookie()
# # # # delete_set_cookie()
# make_uri_content()
# # # # delete_uri_content()
# make_http_url()
# # # # delete_http_url()
# make_http_user_agent()
# # # delete_http_user_agent()
# make_file_content()
# # delete_file_content()
# # # # # delete_file_content()
# make_mime_cust_header()
# # delete_mime_cust_header()
# # # make_file_cmd_val()
# make_http_request_custom_header()
# # delete_http_request_custom_header()
# make_http_response_custom_header()
# # delete_http_response_custom_header()
# make_web_browser()
# # delete_web_browser()
# make_IPS_signature_category_list()
# # delete_IPS_signature_category_list()
# make_IPS_signature_list()
# # delete_IPS_signature_list()
# make_Application_category_list()
# # delete_application_category_list()
# make_application_list()
# # delete_application_list()
# make_application_signature_list()
# # delete_application_signature_list()
# make_log_email_user()
# # delete_log_email_user()
# make_custom_nonen()
# # delete_custom_nonen()
# make_custom_en()
# # delete_custom_en()
