from modules.API.system import StatusApi
from modules.API.system import LicenseApi
from modules.API.system import AdminApi
from modules.API.system import SNMPApi
from modules.API.system import TimeApi
from modules.API.system import ScheduleApi
from modules.API.system import CertificateApi
from modules.API.system import DiagnosticApi
from modules.API.system import PacketmonitorApi
from modules.API.system import RestartApi
from modules.API.system import SettingApi
from modules.API.system import DiagnosticPingApi
from modules.API.system import PacketReplayApi
from modules.API.system import CloudBackupApi
from modules.API.system import OneTouchConfigApi
from modules.API.system import FipsApi
from modules.API.system import NetworkAccessControlApi
import os
from runner.settings import logger
import subprocess
import json


class StatusApi(StatusApi):
    '''SystemApi Class'''


class LicenseApi(LicenseApi):
    '''LicenseApi Class'''


class AdminApi(AdminApi):
    '''AdminApi Class'''


class SNMPApi(SNMPApi):
    '''SNMPApi Class'''


class SettingApi(SettingApi):
    '''SettingSpi Class'''


class TimeApi(TimeApi):
    '''TimeApi Class'''


    def add_interfaces_for_local_ntp_server(self, ifaces, msg=False):
        url = 'api/sonicos/time/local-ntp-server/interfaces'
        input_json = {
            "time": {
                "local_ntp_server":[]
            }
        }
        for iface in ifaces:
            input_json['time']["local_ntp_server"].append({"interface": iface.upper()})
        return self.fw.api_put(url, msg, input_json)
    
    def get_local_ntp_server_interfaces(self):
        url = 'api/sonicos/time/local-ntp-server/interfaces'
        return self.fw.api_get(url)
    
    def delete_interfaces_for_local_ntp_server(self, ifaces, msg=False):
        url = 'api/sonicos/time/local-ntp-server/interfaces'
        input_json = {
            "time": {
                "local_ntp_server":[]
            }
        }
        for iface in ifaces:
            input_json['time']["local_ntp_server"].append({"interface": iface.upper()})
        return self.fw.api_delete(url, msg, input_json)


class ScheduleApi(ScheduleApi):
    '''ScheduleApi Class'''


class CertificateApi(CertificateApi):
    '''CertificateApi Class'''

    def import_cert_local(self, cert_path, name, msg=False, password='password'):
        cert_name = os.path.basename(cert_path)
        if '@' in cert_path:
            clean_path = cert_path.lstrip('@')
        else:
            clean_path = cert_path
        base_url = 'api/sonicos/import/certificates/cert-key-pair/'
        url_put = f'{base_url}name/{name}?{cert_name}'
        #url = 'api/sonicos/import/certificates/cert-key-pair/name/4k?vsftpd_4k.p12'
        with open(clean_path, 'rb') as f:
            cert_data = f.read()
        files = {
                'certPasswd': (None, password),
                'certificate.exp': (cert_name, cert_data, 'application/octet-stream')
            }
        return self.fw.api_put(url_put, msg, files=files)

    def import_cert_local_with_json(self, cert_path, name, password, msg=False):
        url = 'api/sonicos/import/certificates/cert-key-pair/'
        url_put = url + 'name' + '/' + name + '/' + 'password' + '/' + password
        #url = 'api/sonicos/import/certificates/cert-key-pair/name/vsftpd/password/password'
        logger.info(cert_path)
        return self.fw.api_put(url_put, msg, data=cert_path)

    def export_cert_local(self, name, password, msg=False):
        url = 'https://192.168.168.168/api/sonicos/export/certificates/cert-key-pair'
        self.fw.api_login()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "api_export": {
                "cert_key_pair": name,
                "password": password
            }
        }

        json_data = json.dumps(data)
        cert_path = f'/tmp/{name}.pfx'

        # delete previous file
        if os.path.exists(cert_path):
            os.remove(cert_path)

        # construct curl command
        cmd = [
            'curl', '-k', '-i',
            '-H', 'Content-Type: application/json',
            '-H', 'Accept: application/json',
            '-X', 'POST', url,
            '-d', json_data,
            '-o', cert_path
        ]
        logger.info(' '.join(cmd))
        try:
            # execute curl command and get response headers
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and os.path.exists(cert_path):
                logger.info(f'Certificate exported to {cert_path}')
                return cert_path
            else:
                logger.error(f'Export failed: {result.stderr}')
                return None
        except Exception as e:
            logger.error(f'Exception during export: {e}')


class DiagnosticApi(DiagnosticApi):
    '''DiagnosticApi Class'''


class PacketmonitorApi(PacketmonitorApi):
    '''PacketmonitorApi Class'''


class RestartApi(RestartApi):
    '''RestartApi Class'''


class DiagnosticPingApi(DiagnosticPingApi):
    '''DiagnosticPingApi Class'''


class CloudBackupApi(CloudBackupApi):
    '''CloudBackupApi Class'''


class PacketReplayApi(PacketReplayApi):
    '''PacketReplayApi Class'''

    
class OneTouchConfigApi(OneTouchConfigApi):
    '''OneTouchConfigApi Class'''


class FipsApi(FipsApi):
    '''FipsApi Class''' 
    
    
class NetworkAccessControlApi(NetworkAccessControlApi):
    """NetworkAccessControlApi Class"""
 