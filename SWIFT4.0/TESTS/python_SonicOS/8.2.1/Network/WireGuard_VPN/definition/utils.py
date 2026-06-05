from settings import *
import paramiko

def Generatewg0Conf(exportfile):
    #convert tsr to conf file
    with open('/opt/exportfile.conf', 'w') as f:
        f.write(exportfile)
    #modify conf file
    with open('/opt/exportfile.conf', 'r') as r:
        lines = r.readlines()
    with open('/opt/wg0.conf', 'w') as f:
        for line in lines:
            if 'DNS' in line:
                continue
            if 'PersistentKeepalive' in line:
                continue
            if 'PresharedKey' in line:
                continue
            f.write(line)
    #check conf file
    with open('/opt/wg0.conf', 'r') as r:
        lines = r.readlines()
        return True if lines else False

def PutFileToPC2():
    localpath = '/opt/wg0.conf'
    remotepath = '/etc/wireguard/wg0.conf'
    child = paramiko.Transport((PC2_ETH1_IP, 22))
    child.connect(username='root', password='password')
    sftp = paramiko.SFTPClient.from_transport(child)
    sftp.put(localpath, remotepath)
    child.close()

def SetVPNClient():
    pc2login.send_command('wg-quick down wg0')
    pc2login.send_command('wg-quick up wg0')
    showresult = pc2login.send_command('wg show wg0')
    logger.info(showresult)
    return True if 'interface: wg0' in showresult else False

def Checkwg0Traffic(ip):
    checkresult = pc2login.ping_from_eth(ip, 'wg0')
    return checkresult

def Setupwg0ForPC2(exportfile):
    genresult = Generatewg0Conf(exportfile)
    if genresult:
        putresult = PutFileToPC2()
        logger.info(putresult)
        upwgresult = SetVPNClient()
        logger.info(upwgresult)
        return True if upwgresult else False
    else:
        loggin.error('generate wg0 failed in PC1!')
        return False
