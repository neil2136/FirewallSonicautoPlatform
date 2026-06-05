from definition.settings import *


class Local_one_remote_LAN:
    '''
    mode->['NAT','DHCP','PPPoE','Transparent']
    type->['DMZ','Custom']
    side->[0,1]
    LL->['DMZ+Subnets','X3+Subnets']
    LR->['remote_net','remote_trans']
    RL->['LAN Primary Subnet','remote_trans']
    RR->['local_dmz','local_custom']
    '''
    def __init__(self, mode, type, side, LL, LR, RL, RR):
        self.mode = mode
        self.type = type
        self.side = int(side)
        self.LL = LL
        self.LR = LR
        self.RL = RL
        self.RR = RR
        
        self.gw4rmt = Parameter.WANIP
        self.LVPN = {
            'type'              : 'site_to_site',
            'name'              : 'vpn1',
            'enable'            : True,
            'auth_mode'         : 'shared_secret',
            'secret'            : 'password',
            'pri_gate'          : Parameter.REMOTEX1,
            'local_ike_type'    : 'ipv4',
            'peer_ike_type'     : 'ipv4',
            'local_net_type'    : 'name',
            'remote_net_type'   : 'name',
            'local_net_name'    : self.LL,
            'remote_net_name'   : self.LR,
            'ike_exchange'      : 'main',
            'ike_encryption'    : 'aes-128',
            'ipsec_encryption'  : 'aes_128',
            'ike_lifetime'      : '120',
            'ipsec_lifetime'    : '120',
            'keep_alive'        : True,
        }
        self.RVPN = {
            'type'              : 'site_to_site',
            'name'              : 'vpn1',
            'enable'            : True,
            'auth_mode'         : 'shared_secret',
            'secret'            : 'password',
            'pri_gate'          : self.gw4rmt,
            'local_ike_type'    : 'ipv4',
            'peer_ike_type'     : 'ipv4',
            'local_net_type'    : 'name',
            'remote_net_type'   : 'name',
            'local_net_name'    : self.RL,
            'remote_net_name'   : self.RR,
            'ike_exchange'      : 'main',
            'ike_encryption'    : 'aes-128',
            'ipsec_encryption'  : 'aes_128',
            'ike_lifetime'      : '120',
            'ipsec_lifetime'    : '120',
            'keep_alive'        : True,
        }

    def Add_VPN_Policy(self):
        if self.LL == 'DMZ Subnets' or self.LL == 'local_gp':
            self.LVPN['local_net_type'] = 'group'
            self.LVPN['local_net_group'] = self.LVPN.pop('local_net_name')
        if self.LR == 'local_gp2':
            self.LVPN['remote_net_type'] = 'group'
            self.LVPN['remote_net_group'] = self.LVPN.pop('remote_net_name')
        if self.RL == 'DMZ Subnets' or self.RL == 'remote_gp2':
            self.RVPN['local_net_type'] = 'group'
            self.RVPN['local_net_group'] = self.RVPN.pop('local_net_name')
        if self.RR == 'remote_gp':
            self.RVPN['remote_net_type'] = 'group'
            self.RVPN['remote_net_group'] = self.RVPN.pop('remote_net_name')
        rc1 = Lvpn_obj.add_vpn_policy(**self.LVPN)
        rc2 = Rvpn_obj.add_vpn_policy(**self.RVPN)
        return  rc1&rc2

    def Remove_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN Policy'))
        rc1 = Lvpn_obj.del_s2svpn_policy(name = 'vpn1')
        rc2 = Rvpn_obj.del_s2svpn_policy(name = 'vpn1')
        return rc1&rc2

    def Renegotiate_on_local(self):
        logger.info(" {} ".center(20, '-').format('Renegotiate on local'))
        rc = Lvpn_obj.Renegotiate_VPN_Tunnel(**renego_obj)
        return rc

    def Setup_env(self):
        defualt_json = {
                'type':'',
                'comment':'',
                'flow_reporting':True,
                'multicast':False,
                'cos_8021p':False,
                'exclude_route':False,
                'asymmetric_route':False,
                'mgmt_https': True,
                'mgmt_ssh': True,
                'mgmt_snmp': True,
                'mgmt_ping': True,
                'user_https':True,
                'user_http':False
        }
        if self.mode == "DHCP":
            logger.info('Config remote DUT to DHCP mode...')
            opts = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'dhcp',
                'dhcp_hostname' : 'test',
                'dhcp_renew_on_startup':False,
                'dhcp_initiate_renewals_with_discover':False,
                'dhcp_force_discover_interval':0,
            }
            opts.update(defualt_json)
            cmds = ['service dhcpd stop','sleep 2', f'dhcpd -cf {suite_path}/confs/dhcpd.conf']
            cmd = "ping {}  -w 3".format(Parameter.REMOTEX1)
            logger.info('Start DHCP server...')
            PC3.send_commands(cmds)
            logger.info('Config remote DUT WAN with dhcp client mode...')
            rc = Rinterface.config_interface(**opts)
            logger.info("Verify remote DUT WAN get IP...")
            for i in range(10):
                logger.info("send the command {}".format(cmd))
                out = PC1.send_command(cmd)
                if '100% packet loss' not in str(out):
                    logger.info('Send ping from pc1 to remote x1 success')
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            return rc
        elif self.mode == "PPPoE":
            logger.info('Config remote DUT to PPPoE mode...')
            opts1 = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'pppoe',
                'pppoe_user' : 'test',
                'pppoe_passwd' : 'test',
                'pppoe_service':"",
                'pppoe_ip' : Parameter.REMOTEX1 ,
                'pppoe_dynamic': False,
                'pppoe_inactivity': 0,
                'pppoe_lcp_echo_packets': False,
                'pppoe_reconnect': 0,    
            }
            opts2 = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'pppoe',
                'pppoe_user' : 'test',
                'pppoe_passwd' : 'test',
                'pppoe_service':"",
                'pppoe_ip' : Parameter.WANIP ,
                'pppoe_dynamic': False,
                'pppoe_inactivity': 0,
                'pppoe_lcp_echo_packets': False,
                'pppoe_reconnect': 0,    
            }
            opts1.update(defualt_json)
            opts2.update(defualt_json)
            logger.info('Start PPPoE server...')
            cmds = ['pkill pppoe-server',
                    'mv -f /etc/ppp/pppoe-server-options /etc/ppp/pppoe-server-options_bak',
                    'mv -f /etc/ppp/chap-secrets /etc/ppp/chap-secrets_bak',
                    f'cp {suite_path}/confs/pppoe-server-options /etc/ppp/pppoe-server-options',
                    f'cp {suite_path}/confs/chap-secrets /etc/ppp/chap-secrets',
                    f'pppoe-server -I eth1 -L {ppp_server} -R { Parameter.WANIP} -N 2',
                    'echo \"1\" > /proc/sys/net/ipv4/ip_forward']
            cmd = "ping {}  -w 3".format(Parameter.REMOTEX1)
            PC3.send_commands(cmds)
            
            logger.info('Add eth1:1 on pc3 for pppoe traffic...')
            PC3.send_command(f"ifconfig eth1:1 {eth_ip} netmask 255.255.255.0")
            logger.info(f'Config local DUT and Remote WAN to connect to eth1:1 {eth_ip} ...')
            rc = Linterface.config_interface(**opts2)
            time.sleep(8)
            rc &= Rinterface.config_interface(**opts1)
            logger.info("Verify remote DUT WAN get IP...")
            for i in range(10):
                logger.info("send the command {}".format(cmd))
                out = PC1.send_command(cmd)
                if '100% packet loss' not in str(out):
                    logger.info('Send ping from pc1 to remote x1 success')
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            PC3.send_command('echo 1492 > /sys/class/net/ppp0/mtu')
            return rc
        elif self.mode == 'Transparent':
            logger.info('Config remote DUT to Transparent mode...')
            opts = {
                'if' : 'X0',
                'zone': 'LAN' ,
                'mode': 'transparent',
                'transparent_range':{'name': 'remote_trans'},
                'gratuitous_arp_wan_forwarding':False,
                'gratuitous_arp_wan_generation':False,
            }
            opts.update(defualt_json)
            cmds = [f"ifconfig eth0 {trans_ip} netmask 255.255.255.0",
                    f'route add -net 192.168.0.0 netmask 255.255.0.0 gw {Parameter.REMOTEX1}']
            cmd = ["ping {}".format(trans_ip)]
            rc = Rinterface.config_interface(**opts)
            logger.info("Config IP of PC2 which connect to remote DUT...\n")
            PC2.send_commands(cmds)
            logger.info('Verify the traffic between PC2 and remote DUT...')
            PC1.send_command(f"sed -i '/{Parameter.REMOTEX1}/ d' ~/.ssh/known_hosts")
            for i in range(10):
                out = rm_cli.do_cli_commands(cmd)
                if out: 
                    logger.info('Send ping from remote dut to {} success'.format(trans_ip))
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            return rc
        else:
            logger.info('This mode not need to config remote env....')
            return True

    def Restore_env(self):
        default_json= {
                'type':'',
                'comment':'',
                'flow_reporting':True,
                'multicast':False,
                'cos_8021p':False,
                'exclude_route':False,
                'asymmetric_route':False,
                'mgmt_https': True,
                'mgmt_ssh': True,
                'mgmt_snmp': True,
                'mgmt_ping': True,
                'user_https':True,
                'user_http':False
        }
        if self.mode == 'DHCP':
            logger.info('restore remote DUT in DHCP mode...')
            opts = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'static',
                'ip' : Parameter.REMOTEX1,
                'netmask': '255.255.255.0',
                
            }
            opts.update(default_json)
            cmd = "ping {}  -w 3".format(Parameter.REMOTEX1)
            logger.info('Stop DHCP server...')
            PC3.send_commands('service dhcpd stop')
            rc = Rinterface.config_interface(**opts)
            for i in range(10):
                logger.info("send the command {}".format(cmd))
                out = PC1.send_command(cmd)
                if '100% packet loss' not in str(out):
                    logger.info('Send ping from pc1 to remote x1 success')
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            return rc
        elif self.mode == "PPPoE":
            logger.info('Restore remote DUT to PPPoE mode...')
            opts1 = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'static',
                'ip' : Parameter.REMOTEX1,
                'netmask': '255.255.255.0',
            }
            opts2 = {
                'if' : 'X1',
                'zone': 'WAN' ,
                'mode': 'static',
                'ip' : Parameter.WANIP,
                'netmask': '255.255.255.0',
            }
            opts1.update(default_json)
            opts2.update(default_json)
            cmds = ["pkill pppoe-server",
            "mv -f /etc/ppp/pppoe-server-options_bak /etc/ppp/pppoe-server-options",
            "mv -f /etc/ppp/chap-secrets_bak /etc/ppp/chap-secrets"]
            cmd = "ping {}  -w 3".format(Parameter.REMOTEX1)
            logger.info('Restore remote DUT WAN...')
            rc = Rinterface.config_interface(**opts1)
            logger.info("Stop PPPoE server...\n")
            PC3.send_commands(cmds)
            logger.info('Restore local DUT WAN...')
            rc &= Linterface.config_interface(**opts2)
            for i in range(10):
                logger.info("send the command {}".format(cmd))
                out = PC1.send_command(cmd)
                if '100% packet loss' not in str(out):
                    logger.info('Send ping from pc1 to remote x1 success')
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            return rc
        elif self.mode == 'Transparent':
            logger.info('Restore remote DUT to PPPoE mode...')
            opts1 = {
                'if' : 'X0',
                'zone': 'LAN' ,
                'mode': 'static',
                'ip' : Parameter.REMOTEX0,
                'netmask': '255.255.255.0',
            }
            opts1.update(default_json)
            cmds = [
                f'ifconfig eth0 {PC2_IP} netmask 255.255.255.0',
                f"route add -net 192.168.0.0/16 gw {Parameter.REMOTEX0}",
                f"route add -net 12.12.1.0/24 gw {Parameter.REMOTEX0}"]
            cmd = ["ping {}".format(PC2_IP)]
            logger.info('Restore remote DUT WAN...')
            rc = Rinterface.config_interface(**opts1)
            logger.info('------')
            logger.info(rc)
            PC2.send_commands(cmds)
            PC1.send_command(f"sed -i '/{Parameter.REMOTEX1}/ d' ~/.ssh/known_hosts")
            for i in range(10):
                out = rm_cli.do_cli_commands(cmd)
                if out:
                    logger.info('Send ping from remote dut to {} success'.format(PC2_IP))
                    rc &= True
                    break
                elif i == 9:
                    logger.info('Ping failed')
                    rc &= False
            return rc
        else:
            return True
            

    def Test_Log_for_SA_expires(self):
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        time.sleep(125)
        logger.info('Test log to verify VPN policy expires after lifetime runs out')
        res = LogObj.export_log_txt()
        logger.info(res)
        if 'IKE negotiation complete' in res:
            rc &= True
        else:
            rc &= False
        return rc

    def Disable_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Disable VPN Policy ')) 
        ref = copy.deepcopy(self.LVPN)
        ref["enable"] = False
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        return rc

    def Enable_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Enable VPN Policy ')) 
        ref = copy.deepcopy(self.LVPN)
        ref["enable"] = True
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        return rc

    def Verify(self,service,action,type):
        # service-> ["ping","HTTP",'FTP']
        if self.side == 0:
            if type == 'DMZ':
                pc_obj1 = PC4
                pc_obj2 = PC2
                srcIp = PC4_IP
                dstIp = PC2_IP
            elif type == 'Custom':
                pc_obj1 = PCSWAN1
                pc_obj2 = PC2
                srcIp = PCSWAN1_IP
                dstIp = PC2_IP
        elif self.side == 1:
            if type == 'DMZ':
                pc_obj1 = PC4
                pc_obj2 = PC5
                srcIp = PC4_IP
                dstIp = PC5_IP
            elif type == 'Custom':
                pc_obj1 = PC4
                pc_obj2 = PCSWAN2
                srcIp = PC4_IP
                dstIp = PCSWAN2_IP
        elif self.side == 2:
            pc_obj1 = PCSWAN1
            pc_obj2 = PCSWAN2
            srcIp = PCSWAN1_IP
            dstIp = PCSWAN2_IP
        if self.mode == 'Transparent':
            dstIp = "12.12.1.5"
        if service == 'ping':
            res = self.Ping(pc_obj1,srcIp,dstIp)
            if action == 2:
                logger.info('action is allow,ping should pass')
                if res:
                    rc = True
                else:
                    rc = False
            elif action == 0:
                logger.info('action is deny,ping should failed')
                if res:
                    rc = False
                else:
                    rc = True
            return rc
        elif service == 'HTTP':
            url_src = f'http://{srcIp}/' 
            url_dst = f'http://{dstIp}/' 
            logger.info(f"tcpServer to get {url_dst}")
            out1 = pc_obj1.send_command("service httpd start")
            out2 = pc_obj2.send_command("service httpd start")
            msg1 = pc_obj1.send_command(f'curl {url_dst}')
            logger.info(f"tcpServer to get {url_src}")
            msg2 = pc_obj2.send_command(f'curl {url_src}')
            if "HTTP Server Test Page" in msg1 and "HTTP Server Test Page" in msg2:
                res = True
            else:
                res = False
            if action == 2:
                logger.info('action is allow , Connection established and Server side verification  should pass')
                if res:
                    rc = True
                    logger.info("verify http success")
                else:
                    rc = False
                    logger.info("verify http failed")
            elif action == 0:
                logger.info('action is deny,ping should failed')
                if res:
                    rc = False
                    logger.info("verify http success")
                else:
                    rc = True
                    logger.info("verify http failed")
            return rc
        elif service == 'FTP':
            out = pc_obj2.send_command(f"python3 {suite_path}/bin/ftp.py --ip {srcIp} --action {action}")
            logger.info(out)
            if "verify FTP success" in out:
                rc = True
            elif 'verify FTP failed' in out:
                rc = False
            return rc
  
    def Ping(self,pc_obj,src,dst):
        logger.info(f'{pc_obj} send ping src {src} dst {dst}') 
        cmd = f'ping  {dst} -c 5'
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = pc_obj.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to remote x1 success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        return rc

    def tcpServer(self,localaddr,localport):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind((localaddr, localport))
        server_socket.listen(5)
        conn, addr = server_socket.accept()
        logger.info(f'Connection from: {addr}')
        data = conn.recv(128).decode()
        #TBD_SD_11/20/03 To Add Buffering Capabilities on the Server
        ##H323 is a special case for this generic tcp server because of extra-stateful validation at firewall 
        if int(localport) == 1720:
            if data !="0300001c0802403c621c007e000e0528100004c00180050103280001":
                rc  = False
                logger.info("Expected not gotten from client for H323\n")
                logger.info(data)
            else:
                rc = True
                logger.info("Connection established and Server side verification passed\n")
        else:
            if data == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                conn.send("ZYXWVUTSRQPONMLKJIHGFEDCBA")
                rc = True
                logger.info("Connection established and Server side verification passed\n")
            else:
                rc = False
                logger.info("Expected not gotten from client for client")
                logger.info(data)
        conn.close()
        return rc
    
    def tcpClient(self,serveraddr,serverport):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((serveraddr, serverport))
        if int(serverport) == 1720:
            data="0300001c0802403c621c007e000e0528100004c00180050103280001"
        else:
            data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        client_socket.send(data)
        if int(serverport) != 1720:
            msg = client_socket.recv(128).decode()
            if msg == 'ZYXWVUTSRQPONMLKJIHGFEDCBA':
                rc = True
                logger.info("Received expected response data from the server")
                logger.info("Data transfer on TCP Session is verified")
            elif msg == "":
                rc = False
                logger.info("No Response from the server")
            else:
                rc = False
                logger.info("Received response data inconsistent with expected data from the server")
        client_socket.close()
        return rc








        




            



        
            



