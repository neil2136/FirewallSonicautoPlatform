import sys
sys.path.append('/sonicosapiqa/6.5.4/python_lib')

from modules.API.servicegroups import ServiceGroupApi
import sys
import os

import modules.CLI.network

from utm import Firewall
ip = '10.5.182.47'
url = 'api/sonicos/service-groups'
dict = {}
fw = Firewall(ip, user='admin', password='password')
servicegroup = ServiceGroupApi(fw, url)
get_resp = servicegroup.get_servicegroup(url)

def delete_sgroup(name):
    if "service_groups" in get_resp.keys():
        list_service_groups = get_resp["service_groups"]
        for serv_group in list_service_groups:
            if serv_group["name"] == name:
                servicegroup.delete_service_group("name", name, url)
        num_param=1
    elif "service_group" in get_resp.keys():
        service_group = get_resp["service_group"]
        if service_group["name"] == name:
            servicegroup.delete_service_group("name", name, url)
        else:
            pass
    return


def make_delete_group():
    print("entered ")
    service_group = {
        "name": "group1",
        "service_object":[
            {
                "name": "RPC Services"
            },
            {
                "name":"NTP"
            }
        ],
        "service_group":
            [{
                "name": "NetBios"
            },
            {
                "name": "Kerberos"
            }
            ]
    }

    delete_sgroup(service_group["name"])

    uuid, rc_group = servicegroup.config_service_group(url=url, **service_group)

    def edit_by_name():
        json_put = {
            "service_group":{
                "name": "group1",
                "service_object":[
                    {
                        "name":"NTP"
                    }
                ],
                "service_group":[
                    {
                        "name": "NetBios"
                    }
                ]
            }

        }
        put_service_group = servicegroup.put_service_group("name", "group1", json_put, url)
        return

    def edit_by_uuid():
        json_put = {
            "service_group":{
                "name": "group21",
                "service_object":[
                    {
                        "name":"NTP"
                    }
                ],
                "service_group":[
                    {
                        "name": "NetBios"
                    }
                ]
            }

        }
        put_service_group = servicegroup.put_service_group("name", "group1", json_put, url)
        return

    def delete_by_name():
        rc = servicegroup.delete_service_group("name", service_group["name"], url)
        return
    def delete_by_uuid():
        rc = servicegroup.delete_service_group("uuid", uuid, url)
        return

    # edit_by_name()
    # edit_by_uuid()

    # delete_by_name()
    # delete_by_uuid()


make_delete_group()
