import modules.CLI.dpissl
from utm import Firewall
ip = '192.168.168.168'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')


dpisslserver = modules.CLI.dpissl.ServerSslCli(fw)
dpisslclient = modules.CLI.dpissl.ClientSslCli(fw)

# dpissl_dict = {
#     'enable': True,
#     'application-firewall': True,
#     'intrusion-prevention': True,
#     'gateway anti-virus': True,
#     'gateway anti-spyware': True,
#     'include address': 'all',
#     'exclude address': None,
# #    'exclude address type': 'host'
# }
# output1 = dpisslserver.config_general_settings(**dpissl_dict, tag=1)
# print('333333')
# print(output1)
# print('333333')

# output1 = dpisslserver.show_serverssl()
# print('333333')
# print(output1)
# print('333333')


# dpissl_dict = {
#     'ssl-server': '1.1.1.1',
#     'server-type': 'host',
#     'certificate': 'admin'}
#output1 = dpisslserver.add_sslserver(**dpissl_dict, tag=0)
# print('333333')
# print(output1)
# print('333333')


#output1 = dpisslserver.del_sslserver(**dpissl_dict, tag=0)


#output1 = dpisslserver.del_all_sslserver()


#utput1 = dpisslserver.show_serverssl()


# dpissl_dict = {
#     'enable': True,
#     'application-firewall': True,
#     'intrusion-prevention': True,
#     'gateway anti-virus': True,
#     'gateway anti-spyware': True,
#     'include address': '1.1.1.1',
#     'include address type': 'host',
#     'exclude address': '1.1.1.1',
#     'exclude address type': 'host'
# }
# output1 = dpisslclient.config_general_settings(**dpissl_dict, tag=0)
# print('222222')
# print(output1)
# print('222222')


# dpisslclient_dict = {
#     #'resigning-authority': 'Certificate admin'
#     #'resigning-authority': 'default'
#     'resigning-authority': 'default 2048-bit'
# }
# output1 = dpisslclient.config_cert(**dpisslclient_dict)
# print('222222')
# print(output1)
# print('222222')


# dpisslclient_dict = {
#     'exclude address': None,
#     'exclude address type': 'host', #host,network,range,name,group
#     #'exclude service': '1.1.1.1',
#     #'exclude service type': 'host',
#     #'exclude user': '1.1.1.1',
#     #'exclude user type': 'host',
#
# }
# output1 = dpisslclient.config_objects(**dpisslclient_dict)
# print('222222')
# print(output1)
# print('222222')
#
#
# dpisslclient_dict = {
#     'common-name': '1.1.1.1',
#     'action': 'host',
# }
# output1 = dpisslclient.add_commonname(**dpisslclient_dict)


# output1 = dpisslclient.del_commonname('jenny1','jenny2')


# output1 = dpisslclient.del_all_commonname()


#output1 = dpisslclient.show_clientssl()

dpissl_dict2 = {
    'mode': 'include', #include or exclude
    'enable category list':["'1. Violence/Hate/Racism'", "'2. Intimate Apparel/Swimsuit'"],
    #'enable category list':["'1. Violence/Hate/Racism'"],
    #'disable category list':['all']
}
output1 = dpisslclient.config_cfs_category(**dpissl_dict2)
print('333333')
print(output1)
print('333333')
