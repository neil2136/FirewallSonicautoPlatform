from definition.global_v import *
from lib.Dibbler import *

def verify_DHCP_server(case_id):
    logger.info('testcase id is ' + case_id )
    if case_id == '21':
        rc2 = False
        ClearENV('eth0')
        rc = DibblerStart('eth0')
        for i in range(20):
            logger.info("This is the {} time check".format(i))
            time.sleep(30)
            output = os.popen("ifconfig eth0").read()
            logger.info(output)
            if re.search(r'inet6 addr: 2003::[6-9]/64', output, re.I):
                rc2 = True
                break
            else:
                if i == 4:
                    os.system('killall dhclient')
                    time.sleep(2)
                    os.system("dibbler-client stop")
                    time.sleep(2)
                    os.system("dibbler-client start")
                    time.sleep(5)
                    status = os.popen('dibbler-client status').read()
                    logger.info(" {} ".center(20, '-').format(status))
                else:
                    os.system("ip n flush all")
        rc = rc + DibblerStop()
        logger.info(rc)
        ClearENV("eth0")
        return rc2
    elif case_id == '31':
        flag = False
        DibblerStart('eth0')
        for i in range(0,20):
            time.sleep(30)
            output = dhcpserver_obj.get_dhcp_server_leases(version=6)
            logger.info(output)
            if output:
                break
            else:
                if i == 5:
                    DibblerStop()
                    time.sleep(2)
                    ClearENV("eth0")
                    DibblerStart('eth0')
        time1 = output[0]['lease_expires']
        logger.info("1  " + time1)
        time.sleep(70)
        output = dhcpserver_obj.get_dhcp_server_leases(version=6)
        logger.info(output)
        time2 = output[0]['lease_expires']
        logger.info("2  " + time2)
        logger.info(time2)
        DibblerStop()
        if time1 != time2:
            flag = True
        ClearENV("eth0")
        return flag
    elif case_id == '32':
        # This case is designed with dhclient,becauto dibbler can't send release packet 
        flag = False
        ClearENV("eth0")
        if os.path.exists("/tmp/packet.txt"):
            os.system("rm -rf /tmp/packet.txt ")
        os.system('timeout 2 dhclient -6 -r eth0')
        time.sleep(2)
        os.system('killall dhclient')
        time.sleep(2)
        os.system('dhclient -6 -nw eth0')
        for i in range(0,20):
            time.sleep(30)
            logger.info(str(i) + "-" * 60)
            output = os.popen("ifconfig eth0| grep 'inet6 addr.*Global'|awk '{print $3}'").read()
            if output:
                logger.info("successfully bound to lease: " + output)
                logger.info("will start tshark...")
                cmd = "tshark -V -i eth0 '((port 546) or (port 547))' &> /tmp/packet.txt &\n";
                rc = os.system(cmd)
                time.sleep(3)
                logger.info("CLient begin to send dhcpv6 release packet.")
                os.system('dhclient -6 -r eth0')
                os.system('killall dhclient')
                time.sleep(5)
                logger.info("will pkill tshark...")
                os.system('pkill tshark')
                time.sleep(5)
                with open('/tmp/packet.txt', "r", encoding="utf-8") as f:
                    packet_content = f.read()
                logger.info(packet_content)
                if re.search('Message\s*?type:\s*?Release.*?2003::.*?Message\s*?type:\s*?Reply',packet_content,re.S|re.I):
                    flag = True
                    logger.info("find the release reply packet from DUT,PASS...")
                    break
                else:
                    logger.info("Not find the release reply packet from DUT,PASS...")
            else:
                logger.info("ERR: this is the {} time failed to bound any lease...".format(i))
                if os.path.exists("/tmp/packet.txt"):
                    os.system("rm -rf /tmp/packet.txt ")
                ClearENV("eth0")
                os.system('timeout 2 dhclient -6 -r eth0')
                time.sleep(2)
                os.system('killall dhclient')
                time.sleep(2)
                os.system('dhclient -6 -nw eth0')
        return flag
    elif case_id == '45':
        flag = False
        if os.path.exists("/tmp/packet.txt"):
            os.system("rm -rf /tmp/packet.txt ")
        cmd = "tshark -V -i eth0 '((port 546) or (port 547))' &> /tmp/packet.txt &\n";
        rc = os.system(cmd)
        DibblerStart('eth0-stateless')
        ret = os.popen("ps aux|grep dibbler").read()
        logger.info(ret)
        time.sleep(10)
        logger.info("will pkill tshark...")
        rc = rc + os.system('pkill tshark')
        time.sleep(5)
        rc = rc + DibblerStop()
        logger.info(rc)
        with open('/tmp/packet.txt', "r", encoding="utf-8") as f:
            packet_content = f.read()
        logger.info(packet_content)
        if re.search('Message\s*type:\s*Information-request.*Message\s*type:\s*Reply',packet_content,re.S):
            flag = True
        return flag
