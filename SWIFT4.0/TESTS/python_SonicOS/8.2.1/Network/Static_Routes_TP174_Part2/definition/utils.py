import copy

from definition.settings import ao_api, ao_api_remote
from runner.settings import logger


def add_ao(name, zone, ao_type, value, where="local"):
    ao_dic = {
        'name': name,
        'zone': zone,
        'object_type': ao_type,
        'value': value,
    }
    logger.info(f'Add AO {ao_dic} To Remote Firewall...')
    if where == "remote":
        ret = ao_api_remote.config_addressobject(**ao_dic)
    else:
        ret = ao_api.config_addressobject(**ao_dic)
    return ret


def move_priority_from_route(**route_policy):
    logger.info(f'Original route_policy: {route_policy}')
    route_edit = copy.deepcopy(route_policy)
    
    try:
        # Safely get the list of policies; default to empty list if missing
        policies = route_edit.get("route_policies", [])
        
        for _route_edit in policies:
            # Check if "ipv4" exists and is a dictionary
            ipv4_data = _route_edit.get("ipv4")
            
            if isinstance(ipv4_data, dict):
                # Only pop if the key exists to avoid KeyError
                keys_to_remove = ['priority', 'tcp_acceleration', 'probe']
                for key in keys_to_remove:
                    if key in ipv4_data:
                        ipv4_data.pop(key)
                
        logger.info(f'Successfully updated route_edit: {route_edit}')
    except Exception as e:
        # Log the error but return the deepcopied dict to maintain data integrity
        logger.error(f"move_priority_from_route failed due to: {e}")
        
    return route_edit
