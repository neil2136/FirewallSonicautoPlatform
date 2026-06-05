from definition.settings import *


def add_nat_rule(nat_input: dict, msg=False):
    nat_dict = copy.deepcopy(nat_base)
    nat_dict.update(nat_input)
    nat_json = {"nat_policies": [{"ipv4": nat_dict}]}
    if msg:
        return nat_api.add_nat_policy(**nat_json, msg=True)
    nat_api.add_nat_policy(**nat_json)
    out = nat_api.get_nat_policy_by_name(name=nat_input['name'])
    return nat_input['name'] in json.dumps(out)


def edit_nat_rule(nat_name: str, edit_input: dict):
    nat_dict = copy.deepcopy(nat_base)
    nat_dict.update(edit_input)
    nat_json = {"nat_policies": [{"ipv4": nat_dict}]}
    return nat_api.edit_nat_policy_by_name(name=nat_name, **nat_json)
