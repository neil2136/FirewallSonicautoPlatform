from runner.settings import logger
import time
import re

class Switch():
    '''switch class'''
    def __init__(self,fw):
        self.fw=fw

    def add_switch(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('switch' +" "+ str(kwrgs["name"]) )
        for command in kwrgs:
            if command == "stp":
                if kwrgs[command]:
                    commands.append(command)
                else:
                    commands.append("no"+" "+command)
            else:
                commands.append(command + " " + str(kwrgs[command]) )
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def delete_switch(self,switch_name):
        commands = ['config','switch-controller']
        commands.append('no'+" "+'switch' +" "+ switch_name )
        for command in ['commit']:
            commands.append(command)            
            result = self.fw.do_cli_commands(commands)
        time.sleep(3)
        return result

    def edit_switch(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('switch' +" "+ str(kwrgs["name"]) )
        for command in kwrgs:
            if command == "stp-enabled":
                if kwrgs[command]:
                    commands.append(command)
                else:
                    commands.append("no"+" "+command)
            else:
                commands.append(command + " " + str(kwrgs[command]) )
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
            result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def show_switch_detailes(self):
        commands = ['show switch-controller switch']
        output = self.fw.do_cli_commands(commands, tag=1)
        return output


class Port_sw():
    '''port class'''
    def __init__(self,fw):
        self.fw=fw

    def configure_port(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('port' +" "+ str(kwrgs["port"])+" "+'switch' +" "+ str(kwrgs["switch_name"]) )
        del kwrgs['port']
        del kwrgs['switch_name']
        for command in kwrgs:
            if command in ['vlan-trunk','vlan-list','port-8021x guest-vlan','port-8021x radius-vlan-assignment','enable','stp','poe','port-isolation','voice-vlan','portshield','portshield-uplink']:
                if kwrgs[command] :
                    if kwrgs[command]==True:
                        commands.append(command)
                    else:
                        commands.append(command + " " + str(kwrgs[command]) )
                else:
                    commands.append("no"+" "+command)
            else:
                commands.append(command + " " + str(kwrgs[command]) )
        for command in ['commit', 'cancel']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def get_port_info(self,port,switch):
        commands = ['show switch-controller port '+port+' switch '+switch]
        result,output = self.fw.do_cli_commands(commands, tag=1)
        port_data={}
        output=str(output).split("\r\n")
        temp=[]
        re_match="vlan-list|^enable|eblane|stp|poe|^link-speed|^poe-priority|port-isolation|voice-vlan$|^poe-limit-type|power-limit|voice-vlan-cos-mode|bandwidth-ingress|bandwidth-egress|security-count|storm-control|portshield|portshield-uplink|port-8021x|vlan-trunk"
                    
        for key in output:
            if re.search(r'(--MORE--.*)\s*(.*)',key,re.I):
                key=re.search(r'(--MORE.*K\s*)\s(.*)',key,re.I).group(2)
            temp.append(key.strip())
        port_data["port-8021x"]=""

        for line in temp:
            if line =="no enable":
                line="eblane"
            if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I ):
                #print(re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).groups())
                if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(1):
                    if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(1) == "no ":
                        if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3) and re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3):
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)+"-"+re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3)]=False                        
                        
                        else :
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)]=False
                    else:
                        if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3) and re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3):
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)+"-"+re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3)]=True                        
                        
                        else :
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)]=True
                elif re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3):

                    if len(re.search(r'(.*)(%s)\s*(.*)\s*(.*)'%re_match,line, re.I).group(3).split(" "))>1:
                        last_line=""

                        for key in re.search(r'(.*)(%s)\s*(.*)\s*(.*)'%re_match,line, re.I).group(3).split(" ")[0]:
                            last_line=last_line+key
                        port_data[re.search(r'(.*)(%s)\s*(.*)\s*(.*)'%re_match,line, re.I).group(2)+"-"+re.search(r'(.*)(%s)\s*(.*)\s*(.*)'%re_match,line, re.I).group(3).split(" ")[0]]=re.search(r'(.*)(%s)\s*(.*)\s*(.*)'%re_match,line, re.I).group(3).split(" ")[1]

                    else:
                        if re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2) in port_data.keys():
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)+"-"+re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3)]=True
                        else:
                            port_data[re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)]=re.search(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(3)
                else:
                    port_data[re.match(r'(.*)(%s)\s*(.*)'%re_match,line, re.I).group(2)]=True
        if "eblane" in port_data.keys():
            port_data["enable"] = port_data.pop("eblane")
            port_data["enable"]=False
        return port_data

class Network():
    '''Network class'''
    def __init__(self,fw):
        self.fw=fw

    def get_network_info_from_fw(self):
        commands = ['show switch-controller network']
        result,output = self.fw.do_cli_commands(commands, tag=1)
        output=str(output)
        output=output.splitlines()
        network = {}

        for line in output:
            if re.search(r'(network\s+\d+\s+switch\s+[a-zA-Z0-9]*)', line, re.I):
                switch_name = re.search(r'(network\s+(\d+)\s+switch\s+([a-zA-Z0-9]*))', line, re.I).group(3)
                if switch_name not in network.keys():
                    network[switch_name]={}

            if re.search(r'(network\s+\d+\s+switch\s+[a-zA-Z0-9]*)' , line, re.I) :
                vlan_id = re.search(r'(network\s+(\d+)\s+switch\s+([a-zA-Z0-9]*))', line, re.I).group(2)
                ip = 'ip'
                network[switch_name][vlan_id]={}
                network[switch_name][vlan_id][ip]=None
                network[switch_name][vlan_id]["subnetmask"]=None

            if re.search(r'(dhcp|static)' , line, re.I) : 
                mode = 'mode'
                network[switch_name][vlan_id][mode]=re.search(r'(ip\s+(dhcp|static))', line, re.I).group(2)

            if re.search(r'(ip\s+(static|dhcp)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I) :
                ip = 'ip'
                network[switch_name][vlan_id][ip]=re.search(r'(ip\s+(static|dhcp)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(3)

            if re.search(r'(ip\s+(static|dhcp)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I) :
                sub_netmask = 'subnetmask'
                network[switch_name][vlan_id][sub_netmask]=re.search(r'(ip\s+(static|dhcp)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(4)
             
            if re.search(r'(\s+dns\s+(primary)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I) :
                dns_primary_ip = 'dns primary ip'
                network[switch_name][vlan_id][dns_primary_ip]=re.search(r'(\s+dns\s+(primary)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(3)
        
            if re.search(r'(\s+dns\s+(secondary)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I) :
                dns_secondary_ip = 'dns secondary ip'
                network[switch_name][vlan_id][dns_secondary_ip]=re.search(r'(\s+dns\s+(secondary)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))', line, re.I).group(3)
        
        return network
       

    def configure_network(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('network' +" "+ str(kwrgs["vlan_id"])+" "+'switch' +" "+ str(kwrgs["switch_name"]) )
        if "ip" in kwrgs.keys() :
            commands.append('ip' +" "+'static'+" "+ str(kwrgs["ip"])+" "+ str(kwrgs["netmask"]) )
        else:
            commands.append('ip' +" "+'dhcp')

        commands.append('commit')
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def delete_network(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('no network' +" "+ str(kwrgs["vlan_id"])+" "+'switch' +" "+ str(kwrgs["switch_name"]) )
        commands.append('commit')
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def configure_network_dns(self,tag=0,**kwrgs):
        commands = ['config','switch-controller']
        commands.append('network' +" "+ str(kwrgs["vlan_id"])+" "+'switch' +" "+ str(kwrgs["switch_name"]) )
        commands.append('dns' +" "+ str(kwrgs["server_type"])+" "+ str(kwrgs["dns_ip"]))
        commands.append('commit')
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result


class StaticRoutes():
    '''Network class'''
    def __init__(self,fw):
        self.fw=fw

    def get_route_info_from_fw(self):
        commands = ['show switch-controller route']
        result,output = self.fw.do_cli_commands(commands, tag=1)
        output=str(output)
        output=output.splitlines()
        network = {}

        for line in output:
            if re.search(r'(network\s+\d+\s+switch\s+[a-zA-Z0-9]*)', line, re.I):
                switch_name = re.search(r'(network\s+(\d+)\s+switch\s+([a-zA-Z0-9]*))', line, re.I).group(3)
                if switch_name not in network.keys():
                    network[switch_name]={}

            if re.search(r'(network\s+\d+\s+switch\s+[a-zA-Z0-9]*)' , line, re.I) :
                vlan_id = re.search(r'(network\s+(\d+)\s+switch\s+([a-zA-Z0-9]*))', line, re.I).group(2)
                ip = 'ip'
                network[switch_name][vlan_id]={}
                network[switch_name][vlan_id][ip]=None
                network[switch_name][vlan_id]["subnetmask"]=None

            if re.search(r'(dhcp|static)' , line, re.I) : 
                mode = 'mode'
                network[switch_name][vlan_id][mode]=re.search(r'(ip\s+(dhcp|static))', line, re.I).group(2)
    


class Dashboard():
    '''Dashboard class'''
    def __init__(self,fw):
        self.fw=fw
        
    def autoautorize(self,switch):
        commands = ['config','switch-controller']
        commands.append('authorize '+switch)
        for command in [ ' ']:
            commands.append(command)            
            result = self.fw.do_cli_commands(commands)
        return result