import os
import sys
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/confs')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from runner.settings import logger
path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/confs'

def backup_pppoe():
    #--------------------------backup PPPoE confs
    #backup PPPoe -> options
    os.system("\cp -rf /etc/ppp/options  /etc/ppp/options.bak")
    #backup PPPoE -> pppoe-server-options
    os.system("\cp -rf /etc/ppp/pppoe-server-options /etc/ppp/pppoe-server-options.bak")
    #backup chap-secrets
    os.system("\cp -rf /etc/ppp/chap-secrets /etc/ppp/chap-secrets.bak")


def setup_pppoe_server_on_PC1():
    #options
    logger.info("=========================================Setup   options==============================")
    cmd_cp_options = '\cp -rf {}/options  /etc/ppp/options'.format(path)
    os.system(cmd_cp_options)

    #pppoe-server-options
    logger.info("=========================================Setup  pppoe-server-options==============================")
    cmd_cp_pppoe_server = '\cp -rf {}/pppoe-server-options  /etc/ppp/pppoe-server-options'.format(path)
    os.system(cmd_cp_pppoe_server)

    #test   "password"  chap-secrets
    logger.info("=========================================Setup  chap-secrets==============================")
    cmd_cp_chap = '\cp -rf {}/chap-secrets  /etc/ppp/chap-secrets'.format(path)
    os.system(cmd_cp_chap)
    # start PPPoE
    os.system('/usr/sbin/pppoe-server  -I eth2 -L 172.16.1.10 -R 10.10.0.100  -N 20')
    return True


def backup_pptp():
    # --------------------------backup PPTP confs
    #backup -> pptpd.conf
    os.system("\cp -rf /etc/pptpd.conf /etc/pptpd.conf.bak")
    #backup -> options.pptpd
    os.system("\cp -rf /etc/ppp/options.pptpd /etc/ppp/options.pptpd.bak")
    #backup -> pap-secrets
    os.system("\cp -rf /etc/ppp/pap-secrets /etc/ppp/pap-secrets.bak")


def setup_pptp_server_on_PC1():
    #options.pptpd:
    logger.info("=========================================Setup   options.pptpd==============================")
    cmd_cp_pptpd = '\cp -rf {}/options.pptpd  /etc/ppp/options.pptpd'.format(path)
    os.system(cmd_cp_pptpd)

    #pap-secrets:
    logger.info("=========================================Setup  pap-secrets==============================")
    # subprocess.Popen(['cp'] + ['/DEV_TESTS/python_SonicOS/7.0.0/Interface_Quick_smoke/confs/pap-secrets'] + ['/etc/ppp/pap-secrets'], stdout=subprocess.PIPE).communicate()[0]
    # logger.info(''.join(os.popen("cat /etc/ppp/pap-secrets")))
    cmd_cp_pap = '\cp -rf {}/pap-secrets  /etc/ppp/pap-secrets'.format(path)
    os.system(cmd_cp_pap)

    #pptpd.conf:
    logger.info("=========================================Setup  pptpd.conf==============================")
    cmd_cp_pptp_conf = '\cp -rf {}/pptpd.conf  /etc/pptpd.conf'.format(path)
    os.system(cmd_cp_pptp_conf)

    #restart pptpd
    logger.info("======================================Start  PPTP  Server==============================")
    os.system("service pptpd stop")
    output = ''.join(os.popen("service pptpd start"))
    logger.info(output)
    # print(output)
    if 'FAILED' in output:
        return False
    if 'OK' in output:
        return True


def restore_pppoe():
    #restore options
    os.system("\cp -rf /etc/ppp/options.bak  /etc/ppp/options")
    # pppoe-server-options
    os.system("\cp -rf /etc/ppp/pppoe-server-options.bak /etc/ppp/pppoe-server-options")
    #backup chap-secrets
    os.system("\cp -rf /etc/ppp/chap-secrets.bak /etc/ppp/chap-secrets")

def restore_pptp():
    # --------------------------Restore PPTP confs
    # -> pptpd.conf
    os.system("\cp -rf /etc/pptpd.conf.bak /etc/pptpd.conf")
    # -> options.pptpd
    os.system("\cp -rf /etc/ppp/options.pptpd.bak /etc/ppp/options.pptpd")
    # -> pap-secrets
    os.system("\cp -rf /etc/ppp/pap-secrets.bak /etc/ppp/pap-secrets")