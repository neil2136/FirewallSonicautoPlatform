

# common lib change: need modify class InterfaceIPv4Api.config_interface
# from lib.modules.API.network import InterfaceIPv4Api
# def build_json_lan(self, **kwargs):
#     ...
#     elif kwargs['mode'] == 'transparent':
#     json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_transmode(
#         **kwargs)
#     del json_input['interfaces'][0]['ipv4']['routed_mode']

# def _get_interface_transmode(self, **kwargs):
#     wire_json = {}
#     wire_json['transparent'] = {}
#     # transparent mode options
#     try:
#         wire_json['transparent']['transparent_range'] = kwargs['transparent_range']
#         wire_json['transparent']['gratuitous_arp_wan_forwarding'] = kwargs['gratuitous_arp_wan_forwarding']
#         wire_json['transparent']['gratuitous_arp_wan_generation'] = kwargs['gratuitous_arp_wan_generation']
#     except Exception as e:
#         logger.error(repr(e))
#     return wire_json
