import sys
sys.path.append('/sonicosapiqa/6.5.4/python_lib')

from modules.API.servicegroups import ServiceGroupApi
from modules.API.serviceobject import ServiceObjectApi
import sys
import os

import modules.CLI.network

from utm import Firewall
ip = '10.5.182.47'
url = 'api/sonicos/service-groups'
dict = {}
fw = Firewall(ip, user='admin', password='password')
servicegroup = ServiceGroupApi(fw)
get_resp = servicegroup.get_servicegroup)
serviceobject = ServiceObjectApi(fw)
get_resp = serviceobject.get_serviceobject()

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


def delete_sobjects(name):
    num_param = 0
    if "service_objects" in get_resp.keys():
        list_service_objects = get_resp["service_objects"]
        for serv_object in list_service_objects:
            if serv_object["name"] == name:
                serviceobject.delete_service_object("name", name, url)
        num_param=1
    elif "service_object" in get_resp.keys():
        service_object = get_resp["service_object"]
        if service_object["name"] == name:
            num_param = 0
            serviceobject.delete_service_object("name", name, url)
        else:
            num_param =1

def make_delete_objects():

    # custom_object
    service_object_custom = {"object_type": "custom",
                      "name": "custom_try",
                      "custom": 22
                      }
    delete_sobjects(service_object_custom["name"])
    dict[service_object_custom["name"]], rc_custom = serviceobject.config_service_object(url=url, **service_object_custom)
    #icmp_object
    service_object_icmp = {"object_type": "icmp",
                              "name": "icmp_try",
                              "icmp": "echo-reply"
                              }
    delete_sobjects(service_object_icmp["name"])
    dict[service_object_icmp["name"]], rc_icmp = serviceobject.config_service_object(url=url, **service_object_icmp)

    #igmp_object
    service_object_igmp = {"object_type": "igmp",
                      "name": "igmp_trial",
                      "igmp": "v1-member-report"
                      }
    delete_sobjects(service_object_igmp["name"])
    dict[service_object_igmp["name"]], rc_igmp = serviceobject.config_service_object(url=url, **service_object_igmp)

    #tcp_object
    service_object_tcp = {"object_type": "tcp",
                      "name": "tcp_trial",
                      "tcp": {
                          "begin": 33,
                          "end": 40
                      }
                      }
    delete_sobjects(service_object_tcp["name"])
    dict[service_object_tcp["name"]], rc = serviceobject.config_service_object(url=url, **service_object_tcp)

    #udp_object
    service_object_udp = {"object_type": "udp",
                      "name": "udp_trial",
                      "udp": {
                          "begin": 44,
                          "end": 440
                      }
                      }
    delete_sobjects(service_object_udp["name"])
    dict[service_object_udp["name"]], rc = serviceobject.config_service_object(url=url, **service_object_udp)

    #6over4_object
    service_object_6over4 = {"object_type": "6over4",
                  "name": "sixoverfour_try",
                  "6over4": True
                  }
    delete_sobjects(service_object_6over4["name"])
    dict[service_object_6over4["name"]], rc = serviceobject.config_service_object(url=url, **service_object_6over4)

    #gre_object
    service_object_gre = {"object_type": "gre",
                      "name": "gre_try",
                      "gre": True
                      }
    delete_sobjects(service_object_gre["name"])
    dict[service_object_gre["name"]], rc = serviceobject.config_service_object(url=url, **service_object_gre)

    #esp_object
    service_object_esp = {"object_type": "esp",
                      "name": "esp_try",
                      "esp": True
                      }
    delete_sobjects(service_object_esp["name"])
    dict[service_object_esp["name"]], rc = serviceobject.config_service_object(url=url, **service_object_esp)

    #ah_object
    service_object_ah = {"object_type": "ah",
                      "name": "ah_try",
                      "ah": True
                      }
    delete_sobjects(service_object_ah["name"])
    dict[service_object_ah["name"]], rc = serviceobject.config_service_object(url=url, **service_object_ah)

    #eigrp_object
    service_object_eigrp = {"object_type": "eigrp",
                      "name": "eigrp_t",
                      "eigrp": True
                      }
    delete_sobjects(service_object_eigrp["name"])
    dict[service_object_eigrp["name"]], rc = serviceobject.config_service_object(url=url, **service_object_eigrp)

    #l2tp_object
    service_object_l2tp = { "object_type": "l2tp",
                           "name":"l2tp_try",
                           "l2tp": True
        }
    delete_sobjects(service_object_l2tp["name"])
    dict[service_object_l2tp["name"]], rc = serviceobject.config_service_object(url=url, **service_object_l2tp)

    #icmpv6_object
    service_object_icmpv6 = {"object_type": "icmpv6",
                      "name": "icmpv6_try",
                      "icmpv6": "none"
                      }
    delete_sobjects(service_object_icmpv6["name"])
    dict[service_object_icmpv6["name"]], rc = serviceobject.config_service_object(url=url, **service_object_icmpv6)

    #ospf_object
    service_object_ospf = {"object_type": "ospf",
                      "name": "ospf_try",
                      "ospf": "hello"
                      }
    delete_sobjects(service_object_ospf["name"])
    dict[service_object_ospf["name"]], rc = serviceobject.config_service_object(url=url, **service_object_ospf)

    # pim_object
    service_object_pim = {"object_type": "pim",
                      "name": "pim_try",
                      "pim": "hello"
                      }
    delete_sobjects(service_object_pim["name"])
    dict[service_object_pim["name"]], rc = serviceobject.config_service_object(url=url, **service_object_pim)

    def delete_by_uuid():
        for i in dict.values():
            rc = serviceobject.delete_service_object("uuid",i, url)
        return

    def delete_by_name():
        for i in dict.keys():
            print("name",i)
            rc = serviceobject.delete_service_object("name",i, url)
        return

    def edit_object_by_name():
        json_put = {
            "service_object": {
                "name": "custom_try",
                "custom": 55
            }

        }
        put_service_object = serviceobject.put_service_object("name", "custom_try", json_put, url)
        return

    def edit_object_by_uuid():
        json_put = {
            "service_object": {
                "name": "custom_try",
                "custom": 33
            }

        }
        put_service_object = serviceobject.put_service_object("uuid", dict[service_object_custom["name"]], json_put, url)
        return

    # delete_by_uuid()
    # delete_by_name()
    edit_object_by_name()
    # edit_object_by_uuid()


make_delete_objects()

