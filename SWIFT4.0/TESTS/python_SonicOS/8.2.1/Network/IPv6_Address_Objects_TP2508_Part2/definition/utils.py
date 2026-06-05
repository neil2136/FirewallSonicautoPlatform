import json
from definition.settings import addressobj_api
from definition.settings import logger


def compare_ipv6_object_api_return_with_expected(apireturn, expecteddict):
    try:
        objectdetailsapi = apireturn["address_objects"][0]["ipv6"]
        objectdetailsapi.pop("uuid")
        expecteddetails_dict = {
            "name": expecteddict["name"],
            "zone": expecteddict["zone"],
        }
        objecttype = expecteddict["object_type"]
        if objecttype == "host":
            expecteddetails_dict[objecttype] = {"ip": expecteddict["ip"]}
        elif objecttype == "range":
            expecteddetails_dict[objecttype] = {"begin": expecteddict["begin"], "end": expecteddict["end"]}
        elif objecttype == "network":
            expecteddetails_dict[objecttype] = {"subnet": expecteddict["subnet"], "mask": expecteddict["mask"]}
        logger.info(f"object details api is {objectdetailsapi}")
        logger.info(f"expecteddetails_dict is {expecteddetails_dict}")
        return objectdetailsapi == expecteddetails_dict
    except Exception as e:
        logger.error(f"generate compare dict failed: {e}")
        return False


def verify_ao_list_in_ipv4_ipv6_aos(verify_list):
    allv4aos = addressobj_api.get_all_addressobject_ipv4()
    allv6aos = addressobj_api.get_all_addressobject_ipv6()
    verifyrs = []
    if allv4aos and allv6aos:
        all_objects = allv4aos["address_objects"] + allv6aos["address_objects"]
        all_objects_str = json.dumps(all_objects)
        for ao in verify_list:
            if ao in all_objects_str:
                verifyrs.append(True)
            else:
                verifyrs.append(False)
    else:
        verifyrs.append(False)
    return all(verifyrs)
