import copy
import json
import sys
import re
import time
import requests
import urllib3
from runner.settings import logger
from datetime import datetime
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from collections import OrderedDict
# from pdf2image import convert_from_path
# import pytesseract
# from runner.utils.assertion import Assertion

class CTAApi():
    default_cta_report = {
        'locale': "",
        'style': "",
        'snce': 0,
        'report': "",
        'txt': "",
        'comp_name': "",
        'prpr_name': "",
        'phn': "",
        'mail': "",
        'exec_only': 0,
        'app_hlts': 0,
        'thrts': 0,
        'btnt': 0,
        'usr_sesn': 0,
        'rsk_app': 0,
        'mlwr': 0,
        'cntr_trfc': 0,
        'usr_trfc': 0,
        'wb_act': 0,
        'explts': 0,
        'ip_sesn': 0,
        'rprt_cnf': 0,
        'fle_trnsfr': 0,
        'kn_unk_mlwr': 0,
        'ip_trafc': 0,
        'logo': ""

    }
    def __init__(self, fw):
        self.fw = fw
        self.cta = 'api/sonicos/cta-report'
        self.url = 'api/sonicos/administration'
        self.download_cta_url = 'https://192.168.168.168/api/sonicos/export/swarm-report/idx=0&fname=cta-report-'
        self.download_appflow_url ='api/sonicos/appflow/send-report/type=0'

        self.initial_cta_report_json = {
            "cta_report": {
                'locale': "string",
                'style': "string",
                'snce': 0,
                'report': "string",
                'txt': "string",
                'comp_name': "string",
                'prpr_name': "string",
                'phn': "string",
                'mail': "string",
                'exec_only': 0,
                'app_hlts': 0,
                'thrts': 0,
                'btnt': 0,
                'usr_sesn': 0,
                'rsk_app': 0,
                'mlwr': 0,
                'cntr_trfc': 0,
                'usr_trfc': 0,
                'wb_act': 0,
                'explts': 0,
                'ip_sesn': 0,
                'rprt_cnf': 0,
                'fle_trnsfr': 0,
                'kn_unk_mlwr': 0,
                'ip_trafc': 0,
                'logo': "string"
            }
        }

    def download_cta(self, filepath = '/tmp/cta'):
        today = datetime.now()
        formatted_date = today.strftime("%Y%m%d")  # Formatting the date as "YYYYMMDD"
        logger.info(f"Formatted date: {formatted_date}")
        serial_number = self.get_firewall_serial_number()
        file_url = self.download_cta_url + f'{serial_number}-{formatted_date}.pdf'
        headers1 = OrderedDict([('Accept', 'application/json'),
                                          ('Content-Type', 'application/json'),
                                          ('Accept-Encoding', 'application/json'),
                                          ('charset', 'UTF-8')
                                          ])
        payload = ""
        response = requests.get(file_url, auth=("admin", "sonicauto"), data=payload, headers=headers1, verify=False)
        time.sleep(60)
        if response.status_code == 200:
            with open("/tmp/cta.pdf", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            logger.info("File downloaded successfully")
            return True
        else:
            logger.info(f"Failed to download file. Status code: {response.status_code}")
            logger.info(f"Response: {response}")
            return False

    def download_appflow(self,filepath=None):
        file_url = self.download_appflow_url
        # Validate file_url
        if not isinstance(file_url, str):
            logger.info(f"Invalid file URL: {file_url}")
            return False
            # Use /tmp directory if no filepath is provided
        if filepath is None:
            temp_dir = "/tmp"  # Default temporary directory for CentOS
            filepath = os.path.join(temp_dir, "appflow.sfr")

        # Debug filepath
        logger.info(f"filepath: {filepath} (type: {type(filepath)})")

            # Validate filepath
        if not isinstance(filepath, (str, bytes, os.PathLike)):
            print(f"Invalid filepath: {filepath}")
            return False
        try:
            print(f"Downloading from: {file_url}")
            print(f"Saving to: {filepath}")
            payload = ""
            # Make a GET request to download the file
            response = self.fw.api_get(file_url)
            if response:
                with open(filepath, "wb") as file:
                    # Write the content directly
                    file.write(response if isinstance(response, bytes) else response.encode())
                print(f"File downloaded successfully to {filepath}")
                return True
            else:
                print("Failed to download file: Empty response")
                return False
        except Exception as e:
            print(f"An error occurred while downloading the file: {e}")
            return False

    def generate_cta(self, msg=False, **kwargs):
        logger.info("\nGenerate CTA Report\n")
        self.options = dict(CTAApi.default_cta_report)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cta(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)
        cta_report_response = self.fw.api_post(self.cta, msg, data=json_input)
        time.sleep(60)
        return cta_report_response

    def verify_file_sections(self,file_path, section_identifiers):
        """
        Reads a file and verifies if specific sections exist.

        :param file_path: Path to the text file.
        :param section_identifiers: List of section names to verify (without square brackets).
        :return: Dictionary with section identifiers as keys and boolean values indicating presence.
        """
        found_sections = {section: False for section in section_identifiers}

        with open(file_path, 'r') as file:
            content = file.read()
            for section in section_identifiers:
                found_sections[section] = section in content

        return found_sections

    def get_firewall_serial_number(self, msg=False):
        url = self.url + '/global'
        resp = self.fw.api_get(url)
        serial_number = resp['administration']['firewall_name']
        return serial_number

    def get_image_region_by_percentage(self, image, top, bottom, left, right):
        height, width = image.shape  # Get image dimensions
        y1 = int(height * top / 100)
        y2 = int(height * bottom / 100)
        x1 = int(width * left / 100)
        x2 = int(width * right / 100)
        return image[y1:y2, x1:x2]
    
    def get_page_no_by_heading(self, page_heading):
        from pdf2image import convert_from_path
        import numpy as np
        import pytesseract
        import cv2
        pdf_file_path = '/tmp/cta.pdf'
        images = convert_from_path(pdf_file_path)
        all_text = ""
        for image in images:
            img_cv = np.array(image)
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
            section = self.get_image_region_by_percentage(img_gray, top=0, bottom=10, left=0, right=50)
            all_text = pytesseract.image_to_string(section, config="--psm 6")
            all_text = all_text.replace("|", "I")  # 'I' is sometimes converted to '|' by tesseract
            logger.info(f"Page Heading: {all_text}")
            if page_heading in all_text:
                section = self.get_image_region_by_percentage(img_gray, top=95, bottom=100, left=90, right=100)
                all_text = pytesseract.image_to_string(section, config="--psm 6")
                page_no = all_text.split()[1]
                return int(page_no)
    
    def convert_pdf_to_text(self, page_no=0, top=0, bottom=100, left=0, right=100):
        from pdf2image import convert_from_path
        import numpy as np
        import pytesseract
        import cv2
        pdf_file_path = '/tmp/cta.pdf'
        images = convert_from_path(pdf_file_path)
        all_text = ""

        for i, image in enumerate(images):
            if page_no:
                if page_no == i+1:
                    img_cv = np.array(image)
                    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)                
                    section = self.get_image_region_by_percentage(img_gray, top=top, bottom=bottom, left=left, right=right)
                    all_text = pytesseract.image_to_string(section, config="--psm 6")
                    logger.info(all_text)
                    break
                continue
            text = pytesseract.image_to_string(image, config='--psm 6')
            all_text += f"--- Page {i + 1} ---\n"
            all_text += text + "\n"

        # Save the extracted text to a file
        output_file_path = '/tmp/extracted_text.txt'
        with open(output_file_path, 'w') as output_file:
            output_file.write(all_text)
        logger.info(f"Text successfully saved to {output_file_path}")

    def build_json_cta(self, **kwargs):
        json_input = copy.deepcopy(self.initial_cta_report_json)
        logger.info("\n\nInitial Json is :\n")
        logger.info(json_input)
        # Directly assign the sub dictionary to 'cta_report' instead of appending to a list
        json_input['cta_report'] = self.sub_dict(**kwargs)
        return json_input

    def sub_dict(self, **kwargs):
        json_input = {}

        # Check for 'locale' and ensure it's not empty
        json_input['locale'] = ''
        if 'locale' in kwargs and kwargs['locale']:
            json_input['locale'] = kwargs['locale']

        # Check for 'style' and ensure it's not empty
        json_input['style'] = ''
        if 'style' in kwargs and kwargs['style']:
            json_input['style'] = kwargs['style']

        # Check for 'snce' and ensure it's not empty
        json_input['snce'] = 0
        if 'snce' in kwargs and kwargs['snce']:
            json_input['snce'] = kwargs['snce']

        # Check for 'report' and ensure it's not empty
        json_input['report'] = ''
        if 'report' in kwargs and kwargs['report']:
            json_input['report'] = kwargs['report']

        # Check for 'txt' and ensure it's not empty
        json_input['txt'] = ''
        if 'txt' in kwargs and kwargs['txt']:
            json_input['txt'] = kwargs['txt']

        # Check for 'comp_name' and ensure it's not empty
        json_input['comp_name'] = ''
        if 'comp_name' in kwargs and kwargs['comp_name']:
            json_input['comp_name'] = kwargs['comp_name']

        # Check for 'prpr_name' and ensure it's not empty
        json_input['prpr_name'] = ''
        if 'prpr_name' in kwargs and kwargs['prpr_name']:
            json_input['prpr_name'] = kwargs['prpr_name']

        # Check for 'phn' and ensure it's not empty
        json_input['phn'] = ''
        if 'phn' in kwargs and kwargs['phn']:
            json_input['phn'] = kwargs['phn']

        # Check for 'mail' and ensure it's not empty
        json_input['mail'] = ''
        if 'mail' in kwargs and kwargs['mail']:
            json_input['mail'] = kwargs['mail']

        # Check for 'exec_only' and ensure it's not empty
        json_input['exec_only'] = 0
        if 'exec_only' in kwargs and kwargs['exec_only']:
            json_input['exec_only'] = kwargs['exec_only']

        # Continue similarly for the other fields
        json_input['app_hlts'] = 0
        if 'app_hlts' in kwargs and kwargs['app_hlts']:
            json_input['app_hlts'] = kwargs['app_hlts']

        json_input['thrts'] = 0
        if 'thrts' in kwargs and kwargs['thrts']:
            json_input['thrts'] = kwargs['thrts']

        json_input['btnt'] = 0
        if 'btnt' in kwargs and kwargs['btnt']:
            json_input['btnt'] = kwargs['btnt']

        json_input['usr_sesn'] = 0
        if 'usr_sesn' in kwargs and kwargs['usr_sesn']:
            json_input['usr_sesn'] = kwargs['usr_sesn']

        json_input['rsk_app'] = 0
        if 'rsk_app' in kwargs and kwargs['rsk_app']:
            json_input['rsk_app'] = kwargs['rsk_app']

        json_input['mlwr'] = 0
        if 'mlwr' in kwargs and kwargs['mlwr']:
            json_input['mlwr'] = kwargs['mlwr']

        json_input['cntr_trfc'] = 0
        if 'cntr_trfc' in kwargs and kwargs['cntr_trfc']:
            json_input['cntr_trfc'] = kwargs['cntr_trfc']

        json_input['usr_trfc'] = 0
        if 'usr_trfc' in kwargs and kwargs['usr_trfc']:
            json_input['usr_trfc'] = kwargs['usr_trfc']

        json_input['wb_act'] = 0
        if 'wb_act' in kwargs and kwargs['wb_act']:
            json_input['wb_act'] = kwargs['wb_act']

        json_input['explts'] = 0
        if 'explts' in kwargs and kwargs['explts']:
            json_input['explts'] = kwargs['explts']

        json_input['ip_sesn'] = 0
        if 'ip_sesn' in kwargs and kwargs['ip_sesn']:
            json_input['ip_sesn'] = kwargs['ip_sesn']

        json_input['rprt_cnf'] = 0
        if 'rprt_cnf' in kwargs and kwargs['rprt_cnf']:
            json_input['rprt_cnf'] = kwargs['rprt_cnf']

        json_input['fle_trnsfr'] = 0
        if 'fle_trnsfr' in kwargs and kwargs['fle_trnsfr']:
            json_input['fle_trnsfr'] = kwargs['fle_trnsfr']

        json_input['kn_unk_mlwr'] = 0
        if 'kn_unk_mlwr' in kwargs and kwargs['kn_unk_mlwr']:
            json_input['kn_unk_mlwr'] = kwargs['kn_unk_mlwr']

        json_input['ip_trafc'] = 0
        if 'ip_trafc' in kwargs and kwargs['ip_trafc']:
            json_input['ip_trafc'] = kwargs['ip_trafc']

        json_input['logo'] = ''
        if 'logo' in kwargs and kwargs['logo']:
            json_input['logo'] = kwargs['logo']

        return json_input




class AppflowsettingsApi():
    default_options = {
        'connections': 'all',
        'dropped': False,
        'stack': False,
        'ipv6_flows': False,
        #'upload_timeout': 120,
        'real_time': {'data_collection': False},
        'top_applications': False,
        'bits_per_second': False,
        'packets_per_second': False,
        'average_packet_size': False,
        'connections_per_second': False,
        'core_utilization': False,
        'memory_utilization': False,
        'aggregate': {'data_collection': True},
        'applications': True,
        'user': True,
        'ip': True,
        'threat': True,
        'geo_ip': True,
        'url': True,
        'local_collector': False,
        'gifs': True,
        'jpegs': True,
        'pngs': True,
        'js': False,
        'xmls': False,
        'jsons': False,
        'css': False,
        'htmls': True,
        'aspx': True,
        'cms': False,
        # 'geo_ip_resolution': True
    }


    def __init__(self, fw):
        self.fw = fw
        self.appflow_settings = 'api/sonicos/appflow/base'
        self.reset_appflow = 'api/sonicos/appflow/default'
        self.del_reporting = 'api/sonicos/appflow/flow-reporting'
        self.gmsflow_status = 'api/sonicos/reporting/appflow/status/gmsflow-server'
        self.appflow_statistics_ipfix = 'api/sonicos/reporting/appflow/statistics/ipfix'
        self.appflow_statistics_internal = 'api/sonicos/reporting/appflow/statistics/internal'
        self.appflow_statistics_external = 'api/sonicos/reporting/appflow/statistics/external'
        self.default_appflow_json = {
            'appflow': {
                'report': {
                    'connections': 'all',
                    'dropped': False,
                    'stack': False,
                    'ipv6_flows': False,
                   # 'upload_timeout': 70
                },
                'real_time': {
                    'data_collection': False
                },
                'aggregate': {
                    'data_collection': True
                },
                'flows_to': {
                    'local_collector': False
                },
                'geo_ip_resolution': False
            }
        }

    # Building the json for appflow

    def build_json_appflow_settings(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.default_appflow_json)
            logger.info('Appflow json obtained')
            logger.info(json_input)
            if 'connections' or 'dropped' or 'stack' or 'ipv6_flows' in kwargs.keys():
                json_input['appflow']['report']['connections'] = kwargs['connections']
                json_input['appflow']['report']['dropped'] = kwargs['dropped']
                json_input['appflow']['report']['stack'] = kwargs['stack']
                json_input['appflow']['report']['ipv6_flows'] = kwargs['ipv6_flows']
         
            if 'geo_ip_resolution' in kwargs.keys():
                json_input['appflow']['geo_ip_resolution'] = kwargs['geo_ip_resolution']
            if 'local_collector' in kwargs.keys():
                json_input['appflow']['flows_to']['local_collector'] = kwargs['local_collector']
            if 'data_collection_realtime' in kwargs.keys():
                json_input['appflow']['real_time']['data_collection'] = kwargs['data_collection_realtime']
            if 'data_collection_aggregate' in kwargs.keys():
                json_input['appflow']['aggregate']['data_collection'] = kwargs['data_collection_aggregate']
            if 'top_applications' or 'bits_per_second' or 'packets_per_second' or 'average_packet_size' or 'connections_per_second' or 'core_utilization' or 'memory_utilization' in kwargs.keys():
                json_input['appflow']['real_time']['collect_for']={}
                json_input['appflow']['real_time']['collect_for']['top_applications'] = kwargs[
                    'top_applications']
                json_input['appflow']['real_time']['collect_for']['bits_per_second'] = kwargs[
                    'bits_per_second']
                json_input['appflow']['real_time']['collect_for']['packets_per_second'] = kwargs[
                    'packets_per_second']
                json_input['appflow']['real_time']['collect_for']['average_packet_size'] = kwargs[
                    'average_packet_size']
                json_input['appflow']['real_time']['collect_for']['connections_per_second'] = kwargs[
                    'connections_per_second']
                json_input['appflow']['real_time']['collect_for']['core_utilization'] = kwargs[
                    'core_utilization']
                json_input['appflow']['real_time']['collect_for']['memory_utilization'] = kwargs[
                    'memory_utilization']
            if 'applications' or 'user' or 'ip' or 'threat' or 'geo_ip' or 'url' in kwargs.keys():
                json_input['appflow']['aggregate']['collect_for']={} 
                json_input['appflow']['aggregate']['collect_for']['applications'] = kwargs['applications']
                json_input['appflow']['aggregate']['collect_for']['user'] = kwargs['user']
                json_input['appflow']['aggregate']['collect_for']['ip'] = kwargs['ip']
                json_input['appflow']['aggregate']['collect_for']['threat'] = kwargs['threat']
                json_input['appflow']['aggregate']['collect_for']['geo_ip'] = kwargs['geo_ip']
                json_input['appflow']['aggregate']['collect_for']['url']= kwargs['url']
            if 'gifs' or 'jpegs' or 'pngs' or 'js' or 'xmls' or 'jsons' or 'css' or 'html' or 'aspx' or 'cms' in kwargs.keys():
                json_input['appflow']['include_url_types']={}
                json_input['appflow']['include_url_types']['gifs'] = kwargs['gifs']
                json_input['appflow']['include_url_types']['gifs'] = kwargs['jpegs']
                json_input['appflow']['include_url_types']['pngs'] = kwargs['pngs']
                json_input['appflow']['include_url_types']['js'] = kwargs['js']
                json_input['appflow']['include_url_types']['xmls'] = kwargs['xmls']
                json_input['appflow']['include_url_types']['jsons'] = kwargs['jsons']
                json_input['appflow']['include_url_types']['css'] = kwargs['css']
                json_input['appflow']['include_url_types']['html'] = kwargs['html']
                json_input['appflow']['include_url_types']['aspx'] = kwargs['aspx']
                json_input['appflow']['include_url_types']['cms'] = kwargs['cms']
            else:
                logger.info('Not a valid keys for the appflow_setting')
                raise KeyError
        except KeyError:
            logger.error('Error: In creating JSON for Appflow settings')
        return json_input

    # Method to GET all the Appflow settings.
    def retrieve_appflow_settings(self):
        get_response = self.fw.api_get(self.appflow_settings)
        return get_response

    def config_appflow_setting(self, msg=False, **kwargs):
        self.options = dict(AppflowsettingsApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info('options')
        json_input = self.build_json_appflow_settings(**kwargs)
        logger.info(json_input)
        appflow_settings_resp = self.fw.api_put(self.appflow_settings, msg, data=json_input)
        return appflow_settings_resp

    def reset_appflow_default(self, msg=False):
        resp = self.fw.api_post(self.reset_appflow, msg)
        return resp

    def delete_appflow_reporting(self, msg=False):
        response = self.fw.api_delete(self.del_reporting, msg)
        return response

    def retrieve_gmsflow_status(self):
        get_resp1 = self.fw.api_get(self.gmsflow_status)
        return get_resp1

    def retrieve_appflow_stats_ipfix(self):
        get_resp2 = self.fw.api_get(self.appflow_statistics_ipfix)
        return get_resp2
    
    def retrieve_appflow_stats_internal(self):
        get_resp3 = self.fw.api_get(self.appflow_statistics_internal)
        return get_resp3

    def retrieve_appflow_stats_external(self):
        get_resp = self.fw.api_get(self.appflow_statistics_external)
        return get_resp
    
    def visit_cta_report(self):
        url = 'api/sonicos/dynamic-file/checkSwarmReport.json?list=all'
        get_resp = self.fw.api_get(url)
        return get_resp
#######################GmsFlow Server API########################################

class GmsflowreportingApi():
      
      default_options = {
        'flows': False,
        'real_time': 'false'
         }
      def __init__(self, fw):
            self.fw=fw 
            self.gmsflow_server = 'api/sonicos/appflow/gmsflow-server/base'
            self.intial_gmsflow_json_basic={
                    "appflow": {
                            "gmsflow_server": {
                                   "flows": False,
                                    "real_time": False,
                                    "system_logs": True,
                                    "report": {
                                    "open": False,
                                    "close": True,
                                    "update": {
                                          "threat": False,
                                          "application": False,
                                          "user": False,
                                          "vpn_tunnel": False,
                                          "url": False
                                               }
                                      },
                                    "reporting_format": "ipfix-with-extension",
                                    "dynamic_flows": {
                                         "connections": True,
                                         "users": True,
                                         "urls": True,
                                         "url_ratings": True,
                                         "vpns": True,
                                         "devices": True,
                                         "spams": True,
                                         "locations": True,
                                         "voips": True
                                           },
                                    "mode": "basic",
                                    "auto_synchronize": True,
                                    #"advanced_mode": "active-standby",
                                    "server_ip": {
                                         "server": {
                                              "ip": {}
                                            },
                                          "vpn_source_ip": {},
                                          "communication_timeout": 60
                                          }
                                    #"server_2_ip": {
                                    #     "server": {
                                    #          "ip": {}
                                    #        },
                                    #     "vpn_source_ip": {},
                                    #     "communication_timeout": 60
                                    #}
                          }
                    }
               }
     
            self.intial_gmsflow_json_advanced={
                    "appflow": {
                            "gmsflow_server": {
                                   "flows": False,
                                    "real_time": False,
                                    "system_logs": True,
                                    "report": {
                                    "open": False,
                                    "close": True,
                                    "update": {
                                          "threat": False,
                                          "application": False,
                                          "user": False,
                                          "vpn_tunnel": False,
                                          "url": False
                                               }
                                      },
                                    "reporting_format": "ipfix-with-extension",
                                    "dynamic_flows": {
                                         "connections": True,
                                         "users": True,
                                         "urls": True,
                                         "url_ratings": True,
                                         "vpns": True,
                                         "devices": True,
                                         "spams": True,
                                         "locations": True,
                                         "voips": True
                                           },
                                    "mode": "advanced",
                                    "auto_synchronize": True,
                                    "advanced_mode": "active-standby",
                                    "server_ip": {
                                         "server": {
                                              "ip": {}
                                            },
                                          "vpn_source_ip": {},
                                          "communication_timeout": 60
                                          },
                                    "server_2_ip": {
                                         "server": {
                                              "ip": {}
                                            },
                                         "vpn_source_ip": {},
                                         "communication_timeout": 60
                                     }
                          }
                    }
               }
      
      def get_gmsflow_reporting(self):
         get_response = self.fw.api_get(self.gmsflow_server)
         return get_response
      
      def config_gmsflow_server_basic(self,msg=False,**kwargs):
         json_input={}
         try:
             json_input=copy.deepcopy(self.intial_gmsflow_json_basic)
             if 'flows' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['flows']=kwargs['flows']
             if 'real_time' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['real_time']=kwargs['real_time']
             if 'system_logs' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['system_logs']=kwargs['system_logs']  
             if 'open' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['report']['open']=kwargs['open']
             if 'close' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['report']['close']=kwargs['close'] 
             gms_update=json_input['appflow']['gmsflow_server']['report']['update']
             if 'threat' in kwargs.keys():
                 gms_update['threat']=kwargs['threat']
             if 'application' in kwargs.keys():
                 gms_update['application']=kwargs['application']
             if 'user' in kwargs.keys():
                 gms_update['user']=kwargs['user']
             if 'vpn_tunnel' in kwargs.keys():
                 gms_update['vpn_tunnel']=kwargs['vpn_tunnel']
             if 'url' in kwargs.keys():
                 gms_update['url']=kwargs['url']
             if 'reporting_format' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['reporting_format']=kwargs['reporting_format']
             gms_dynamic=json_input['appflow']['gmsflow_server']['dynamic_flows']
             if 'connections' in kwargs.keys():
                 gms_dynamic['connections']=kwargs['connections']
             if 'dynamic_users' in kwargs.keys():
                 gms_dynamic['users']=kwargs['dynamic_users']
             if 'dynamic_urls' in kwargs.keys():
                 gms_dynamic['urls']=kwargs['dynamic_urls']
             if 'url_ratings' in kwargs.keys():
                 gms_dynamic['url_ratings']=kwargs['url_ratings']
             if 'vpns' in kwargs.keys():
                 gms_dynamic['vpns']=kwargs['vpns']
             if 'devices' in kwargs.keys():
                 gms_dynamic['devices']=kwargs['devices']
             if 'spams' in kwargs.keys():
                 gms_dynamic['spams']=kwargs['spams']
             if 'locations' in kwargs.keys():
                 gms_dynamic['locations']=kwargs['locations']
             if 'voips' in kwargs.keys():
                 gms_dynamic['voips']=kwargs['voips']
             if 'mode' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['mode']=kwargs['mode']
             if 'auto_sync' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['auto_synchronize']=kwargs['auto_sync']
             if 'ip' in kwargs.keys():
                 #json_input['appflow']['gmsflow_server']['server_ip']['server']['ip']={}
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['ip']['value']=kwargs['ip']                     
             if 'address' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['address']={}
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['address']['name']=kwargs['address']
             if 'vpn_source' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['vpn_source_ip']['vlaue']=kwargs['vpn_source']
             if 'timeout' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['communication_timeout']=kwargs['timeout']                                                                                     
         except KeyError:
               logger.info('error while creating basic gmsflow json')
         gmsflowserver_resp = self.fw.api_put(self.gmsflow_server, msg, data=json_input)
         return gmsflowserver_resp


      def config_gmsflow_server_advance(self,msg=False,**kwargs):
         json_input={}
         try:
             json_input=copy.deepcopy(self.intial_gmsflow_json_advanced)
             if 'flows' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['flows']=kwargs['flows']
             if 'real_time' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['real_time']=kwargs['real_time']
             if 'system_logs' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['system_logs']=kwargs['system_logs']  
             if 'open' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['report']['open']=kwargs['open']
             if 'close' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['report']['close']=kwargs['close'] 
             gms_update=json_input['appflow']['gmsflow_server']['report']['update']
             if 'threat' in kwargs.keys():
                 gms_update['threat']=kwargs['threat']
             if 'application' in kwargs.keys():
                 gms_update['application']=kwargs['application']
             if 'user' in kwargs.keys():
                 gms_update['user']=kwargs['user']
             if 'vpn_tunnel' in kwargs.keys():
                 gms_update['vpn_tunnel']=kwargs['vpn_tunnel']
             if 'url' in kwargs.keys():
                 gms_update['url']=kwargs['url']
             if 'reporting_format' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['reporting_format']=kwargs['reporting_format']
             gms_dynamic=json_input['appflow']['gmsflow_server']['dynamic_flows']
             if 'connections' in kwargs.keys():
                 gms_dynamic['connections']=kwargs['connections']
             if 'dynamic_users' in kwargs.keys():
                 gms_dynamic['users']=kwargs['dynamic_users']
             if 'dynamic_urls' in kwargs.keys():
                 gms_dynamic['urls']=kwargs['dynamic_urls']
             if 'url_ratings' in kwargs.keys():
                 gms_dynamic['url_ratings']=kwargs['url_ratings']
             if 'vpns' in kwargs.keys():
                 gms_dynamic['vpns']=kwargs['vpns']
             if 'devices' in kwargs.keys():
                 gms_dynamic['devices']=kwargs['devices']
             if 'spams' in kwargs.keys():
                 gms_dynamic['spams']=kwargs['spams']
             if 'locations' in kwargs.keys():
                 gms_dynamic['locations']=kwargs['locations']
             if 'voips' in kwargs.keys():
                 gms_dynamic['voips']=kwargs['voips']
             if 'mode' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['mode']=kwargs['mode']
             if 'auto_sync' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['auto_synchronize']=kwargs['auto_sync']
             if 'ip' in kwargs.keys():
                 #json_input['appflow']['gmsflow_server']['server_ip']['server']['ip']={}
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['ip']['value']=kwargs['ip']                     
             if 'address' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['address']={} 
                 json_input['appflow']['gmsflow_server']['server_ip']['server']['address']['name']=kwargs['address']
             if 'vpn_source' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['vpn_source_ip']['value']=kwargs['vpn_source']
             if 'timeout' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_ip']['communication_timeout']=kwargs['timeout']                                                                                     
             if 'ip_2' in kwargs.keys():
                 #json_input['appflow']['gmsflow_server']['server_2_ip']['server']['ip']={}
                 json_input['appflow']['gmsflow_server']['server_2_ip']['server']['ip']['value']=kwargs['ip_2']                     
             if 'address_2' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_2_ip']['server']['address']={}  
                 json_input['appflow']['gmsflow_server']['server_2_ip']['server']['address']['name']=kwargs['address_2']
             if 'vpn_source_2' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_2_ip']['vpn_source_ip']['value']=kwargs['vpn_source_2']
             if 'timeout_2' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['server_2_ip']['communication_timeout']=kwargs['timeout_2']                                                                                     
             if 'advance_mode' in kwargs.keys():
                 json_input['appflow']['gmsflow_server']['advanced_mode']=kwargs['advance_mode']
         except KeyError:
               logger.info('error while creating advance gmsflow json')
         gmsflowserver_resp = self.fw.api_put(self.gmsflow_server, msg, data=json_input)
         return gmsflowserver_resp

                          
#################Appflow Server API###############
#########

class AppflowserverApi():
    ####### '''Reports Defualt Option''' ##########
    # 'open': False,
    # 'close': True,
    ######### ''' Update Default Option ''' ##########
    # 'threat': False,
    # 'application': False,
    # 'user': False,
    # 'vpn_tunnel': False,
    # 'url': False,
    ######### ''' Dynamic Flows Default Option ''' ##########
    # 'connections': True,
    # 'users': True,
    # 'urls': True,
    # 'url_ratings': True,
    # 'vpns': True,
    # 'devices': True,
    # 'spams': True,
    # 'locations': True,
    # 'voips': True,
    ########## ''' Server IP Default Option ''' #########
    # 'keep_alive': false
    # 'ip': '0.0.0.0',
    # 'vpn_source_ip': '0.0.0.0',
    # 'max_flows': 200000
    # 'communication_timeout': 60,
    # 'firewall_name': 'My SonicWall'
    # 'passphrase': 'None',
    # 'auto_synchronize': True

    default_options = {
        'flows': False,
        'real_time': 'false',

    }

    def __init__(self, fw):
        self.fw = fw
        self.appflow_server = 'api/sonicos/appflow/appflow-server'
        self.initial_appflow_server_json = {
            'appflow': {
                'appflow_server': {
                    'flows': False,
                    'real_time': False,
                    'system_logs': True,
                    'report': {
                        'open': False,
                        'close': True,
                        'update': {}

                    },
                    'dynamic_flows': {},
                    'server_ip': {},
                    'server_2_ip': {}
                }
            }
        }

    def build_json_appflow_server(self, **kwargs):

        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_appflow_server_json)
            if 'flows' in kwargs.keys():
                json_input['appflow']['appflow_server']['flows'] = kwargs['flows']
            if 'real_time' in kwargs.keys():
                json_input['appflow']['appflow_server']['real_time'] = kwargs['real_time']
            if 'system_logs' in kwargs.keys():
                json_input['appflow']['appflow_server']['system_logs'] = kwargs['system_logs']
            if 'open' in kwargs.keys():
                json_input['appflow']['appflow_server']['report']['open'] = kwargs['open']
            if 'close' in kwargs.keys():
                json_input['appflow']['appflow_server']['report']['close'] = kwargs['close']

            if 'threat' or 'application' or 'update_user' or 'vpn_tunnel' or 'update.url' in kwargs.keys():
                json_input['appflow']['appflow_server']['report']['update']['threat'] = kwargs['threat']
                json_input['appflow']['appflow_server']['report']['update']['application'] = kwargs['application']
                json_input['appflow']['appflow_server']['report']['update']['user'] = kwargs['update_user']
                json_input['appflow']['appflow_server']['report']['update']['vpn_tunnel'] = kwargs['vpn_tunnel']
                json_input['appflow']['appflow_server']['report']['update']['url'] = kwargs['update_url']
            if 'connections' or 'dynamic_users' or 'dynamic_url' or 'url_ratings' or 'vpns' or 'devices' or 'spams' or 'locations' or 'voips' in kwargs.keys():
                json_input['appflow']['appflow_server']['dynamic_flows']['connections'] = kwargs['connections']
                json_input['appflow']['appflow_server']['dynamic_flows']['users'] = kwargs['dynamic_users']
                json_input['appflow']['appflow_server']['dynamic_flows']['urls'] = kwargs['dynamic_urls']
                json_input['appflow']['appflow_server']['dynamic_flows']['url_ratings'] = kwargs['url_ratings']
                json_input['appflow']['appflow_server']['dynamic_flows']['vpns'] = kwargs['vpns']
                json_input['appflow']['appflow_server']['dynamic_flows']['devices'] = kwargs['devices']
                json_input['appflow']['appflow_server']['dynamic_flows']['spams'] = kwargs['spams']
                json_input['appflow']['appflow_server']['dynamic_flows']['locations'] = kwargs['locations']
                json_input['appflow']['appflow_server']['dynamic_flows']['voips'] = kwargs['voips']
            if 'ip_1' or 'vpn_source_ip_1' or 'communication_timeout_1' or 'max_flows_1' or 'firewall_name_1' or 'passphrase_1' or 'address_1' in kwargs.keys():
                json_input['appflow']['appflow_server']['server_ip']['server']['ip']['value'] = kwargs['ip_1']
                json_input['appflow']['appflow_server']['server_ip']['server']['address']['name'] = kwargs['address_1']
                json_input['appflow']['appflow_server']['server_ip']['vpn_source_ip']['value'] = kwargs[
                    'vpn_source_ip_1']
                json_input['appflow']['appflow_server']['server_ip']['max_flows'] = kwargs['max_flows_1']
                json_input['appflow']['appflow_server']['server_ip']['communication_timeout'] = kwargs[
                    'communication_timeout_1']
                json_input['appflow']['appflow_server']['server_ip']['firewall_name'] = kwargs['firewall_name_1']
                json_input['appflow']['appflow_server']['server_ip']['passphrase'] = kwargs['passphrase_1']

            if 'ip_2' or 'vpn_source_ip_2' or 'communication_timeout_2' or 'max_flows_2' or 'firewall_name_2' or 'passphrase_2' or 'address_2' in kwargs.keys():
                json_input['appflow']['appflow_server']['server_2_ip']['server']['ip']['value'] = kwargs['ip_2']
                json_input['appflow']['appflow_server']['server_2_ip']['server']['address']['name'] = kwargs[
                    'address_2']
                json_input['appflow']['appflow_server']['server_2_ip']['vpn_source_ip']['value'] = kwargs[
                    'vpn_source_ip_2']
                json_input['appflow']['appflow_server']['server_2_ip']['max_flows'] = kwargs['max_flows_2']
                json_input['appflow']['appflow_server']['server_2_ip']['communication_timeout'] = kwargs[
                    'communication_timeout_2']
                json_input['appflow']['appflow_server']['server_2_ip']['firewall_name'] = kwargs['firewall_name_2']
                json_input['appflow']['appflow_server']['server_2_ip']['passphrase'] = kwargs['passphrase_2']

            if 'keep_alive' in kwargs.keys():
                json_input['appflow']['appflow_server']['keep_alive'] = kwargs['keep_alive']
            if 'mode' in kwargs.keys():
                json_input['appflow']['appflow_server']['mode'] = kwargs['mode']
            if 'auto_synchronize' in kwargs.keys():
                json_input['appflow']['appflow_server']['server_ip']['auto_synchronize'] = kwargs['auto_synchronize']
            if 'load_balance_mode' in kwargs.keys():
                json_input['appflow']['appflow_server']['load_balancing_mode'] = kwargs['load_balance_mode']
            else:
                logger.info('Not a valid appflow server key')

        except KeyError:
            logger.error('Error: missing appflow server key')

        return json_input

    def get_appflow_server(self):
        get_response = self.fw.api_get(self.appflow_server)
        return get_response

    def config_appflow_server(self, msg=False, **kwargs):
        self.options = dict(AppflowserverApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info('options')
        json_input = self.build_json_appflow_server(**kwargs)
        logger.info(json_input)
        appflowserver_resp = self.fw.api_put(self.appflow_server, msg, data=json_input)
        return appflowserver_resp


############################External Collector API#################################################

class ExternalcollectorApi():
    ####### '''Reports Defualt Option''' ##########
    # 'open': False,
    # 'close': True,
    # 'active_timeout': 0
    # 'kilobytes_exchanged':{}
    ######### ''' Update Default Option ''' ##########
    # 'threat': False,
    # 'application': False,
    # 'user': False,
    # 'vpn_tunnel': False,
    # 'url': False

    default_options = {
        'flows': False,
        'reporting_format': 'netflow-5',
        'ip': '0.0.0.0',
        'vpn_source_ip': '0.0.0.0',
        'port': 2055,
        'kilobytes_exchanged': {}
        # 'kilobytes': None,
        # 'once': False

    }

    def __init__(self, fw):
        self.fw = fw
        self.external_collector_url = 'api/sonicos/appflow/external-collector/base'
        self.initial_external_collector_json = {
            'appflow': {
                'external_collector': {
                    'flows': False,
                    'reporting_format': None,
                    'ip': '0.0.0.0',
                    'vpn_source_ip': '0.0.0.0',
                    'port': 2055,
                    'report': {
                        'open': True,
                        'close': True,
                        'active_timeout': 0,
                        'kilobytes_exchanged': {},
                        'update': {
                            'threat': True,
                            'application': True,
                            'user': True,
                            'vpn_tunnel': True,
                            'url': True
                        }
                    }
                }
            }
        }

    def build_json_external_collector(self, **kwargs):

        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_external_collector_json)
            if 'flows' in kwargs.keys():
                json_input['appflow']['external_collector']['flows'] = kwargs['flows']
            if 'reporting_format' in kwargs.keys():
                json_input['appflow']['external_collector']['reporting_format'] = kwargs['reporting_format']
            try:
                if kwargs['reporting_format'] == 'netflow-5' or 'netflow-9' or 'ipfix' or 'ipfix-with-extensions':
                    json_input['appflow']['external_collector']['server']['ip']['value'] = kwargs['ip']
                    json_input['appflow']['external_collector']['server']['address']['name'] = kwargs['address']
                    json_input['appflow']['external_collector']['vpn_source_ip']['value'] = kwargs['vpn_source_ip']
                    json_input['appflow']['external_collector']['port'] = kwargs['port']
                else:
                    raise ValueError
            except ValueError:
                logger.info('Reporting format has not valid value')

            try:
                if kwargs['reporting_format'] == 'netflow-5' or 'netflow-9' or 'ipfix' or 'ipfix-with-extensions':
                    if 'open' in kwargs.keys():
                        json_input['appflow']['external_collector']['report']['open'] = kwargs['open']
                    if 'close' in kwargs.keys():
                        json_input['appflow']['external_ccllector']['report']['close'] = kwargs['close']
                    if 'active_timeout' or 'kilobytes_exchanged' in kwargs.keys():
                        try:
                            if 'active_timeout' in json_input['appflow']['external_collector']['report']:
                                json_input['appflow']['external_collector']['report'].pop('kilobytes_exchanged')
                                json_input['appflow']['external_collector']['report']['active_timeout'] = kwargs[
                                    'active_timeout']
                            if 'kilobytes' or 'once' in json_input['appflow']['external_collector']['report']:
                                json_input['appflow']['external_collector']['report'].pop('active_timeout')
                                json_input['appflow']['external_collector']['report']['kilobytes_exchanged'][
                                    'kilobytes'] = kwargs['kilobytes']
                                json_input['appflow']['external_collector']['report']['kilobytes_exchanged']['once'] = \
                                kwargs['once']
                            else:
                                raise ValueError
                        except ValueError:
                            logger.error(
                                'Report connection on active timeout has been enabled, please disable it first')
                    if 'threat' or 'application' or 'user' or 'vpn_tunnel' or 'url' in kwargs.keys():
                        json_input['appflow']['external_collector']['report']['update']['threat'] = kwargs['threat']
                        json_input['appflow']['external_collector']['report']['update']['application'] = kwargs[
                            'application']
                        json_input['appflow']['external_collector']['report']['update']['user'] = kwargs['user']
                        json_input['appflow']['external_collector']['report']['update']['vpn_tunnel'] = kwargs[
                            'vpn_tunnel']
            except KeyError:
                logger.error('Midding report key in external collector')
            try:
                if kwargs['reporting_format'] == 'netflow-9' or 'ipfix' or 'ipfix-with-extensions':
                    json_input['appflow']['external_collector']['send'] = {}
                    if 'templates' in kwargs.keys():
                        json_input['appflow']['external_collector']['send']['templates'] = kwargs['templates']
                else:
                    raise KeyError
            except KeyError:
                pass
                logger.error('Missing templates key in netflow-9')

            try:
                if kwargs['reporting_format'] == 'ipfix-with-extensions':
                    if 'templates' in kwargs.keys():
                        json_input['appflow']['external_collector']['send']['static_flows'] = kwargs['static_flows']
                    json_input['appflow']['external_collector']['static_flows'] = {}
                    try:
                        if 'applications' or 'viruses' or 'spyware' or 'intrusions' or 'location_map' or 'services' or 'rating_map' or 'table_map' or 'column_map' in kwargs.keys():
                            json_input['appflow']['external_collector']['static_flows']['applications'] = kwargs[
                                'applications']
                            json_input['appflow']['external_collector']['static_flows']['viruses'] = kwargs['viruses']
                            json_input['appflow']['external_collector']['static_flows']['spyware'] = kwargs['spyware']
                            json_input['appflow']['external_collector']['static_flows']['intrusions'] = kwargs[
                                'intrusions']
                            json_input['appflow']['external_collector']['static_flows']['location_map'] = kwargs[
                                'location_map']
                            json_input['appflow']['external_collector']['static_flows']['services'] = kwargs['services']
                            json_input['appflow']['external_collector']['static_flows']['rating_map'] = kwargs[
                                'rating_map']
                            json_input['appflow']['external_collector']['static_flows']['table_map'] = kwargs[
                                'table_map']
                            json_input['appflow']['external_collector']['static_flows']['column_map'] = kwargs[
                                'column_map']
                        else:
                            raise KeyError
                    except KeyError:
                        logger.info('Passing the unassigned key ')
                        pass

                    try:
                        json_input['appflow']['external_collector']['dynamic_flows'] = {}
                        if 'connections' or 'users' or 'urls' or 'url_ratings' or 'vpns' or 'devices' or 'spams' or 'locations' or 'voips' in kwargs.keys():
                            json_input['appflow']['external_collector']['dynamic_flows']['connections'] = kwargs[
                                'connections']
                            json_input['appflow']['external_collector']['dynamic_flows']['users'] = kwargs['users']
                            json_input['appflow']['external_collector']['dynamic_flows']['urls'] = kwargs['urls']
                            json_input['appflow']['external_collector']['dynamic_flows']['url_ratings'] = kwargs[
                                'url_ratings']
                            json_input['appflow']['external_collector']['dynamic_flows']['vpns'] = kwargs['vpns']
                            json_input['appflow']['external_collector']['dynamic_flows']['devices'] = kwargs['devices']
                            json_input['appflow']['external_collector']['dynamic_flows']['spams'] = kwargs['spams']
                            json_input['appflow']['external_collector']['dynamic_flows']['locations'] = kwargs[
                                'locations']
                            json_input['appflow']['external_collector']['dynamic_flows']['voips'] = kwargs['voips']
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                        # logger('Error while creating dynamic_flows keys')
                    try:
                        json_input['appflow']['external_collector']['ipfix_reports'] = {}
                        if 'top_10_apps' or 'interface_statistics' or 'core_utilization' or 'memory_utilization' or 'system_logs' or 'sdwan_probe':
                            json_input['appflow']['external_collector']['ipfix_reports']['top_10_apps'] = kwargs[
                                'top_10_apps']
                            json_input['appflow']['external_collector']['ipfix_reports']['interface_statistics'] = \
                            kwargs['interface_statistics']
                            json_input['appflow']['external_collector']['ipfix_reports']['core_utilization'] = kwargs[
                                'core_utilization']
                            json_input['appflow']['external_collector']['ipfix_reports']['memory_utilization'] = kwargs[
                                'memory_utilization']
                            json_input['appflow']['external_collector']['ipfix_reports']['system_logs'] = kwargs[
                                'system_logs']
                            json_input['appflow']['external_collector']['ipfix_reports']['sdwan_probe'] = kwargs[
                                'sdwan_probe']
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                        # logger('Error while creating ipfix_reports keys')

            except KeyError:
                logger.error('Error while creating reporting_format keys ')

        except KeyError:
            logger.error('Error: in creating External Collector JSON')

        return json_input

    def get_appflow_server(self):
        get_response = self.fw.api_get(self.external_collector_url)
        return get_response

    def config_external_collector(self, msg=False, **kwargs):
        self.options = dict(ExternalcollectorApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info('options')
        json_input = self.build_json_external_collector(**kwargs)
        logger.info(json_input)
        external_collector_resp = self.fw.api_put(self.external_collector_url, msg, data=json_input)
        return external_collector_resp

    def edit_external_collector(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.external_collector_url, msg, data=json_input)
        return resp

class SynchronizeApi():
    '''SynchronizeApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/appflow/appflow-server/server-ip/synchronize'
        self.url1 = 'api/sonicos/appflow/appflow-server/server-ip/synchronize-logs'
        self.url2 = 'api/sonicos/appflow/appflow-server/server-ip/test-connectivity'

        self.url3 = 'api/sonicos/appflow/appflow-server/server-2-ip/synchronize'
        self.url4 = 'api/sonicos/appflow/appflow-server/server-2-ip/synchronize-logs'
        self.url5 = 'api/sonicos/appflow/appflow-server/server-2-ip/test-connectivity'

        self.url6 = 'api/sonicos/appflow/gmsflow-server/server-ip/synchronize'
        self.url7 = 'api/sonicos/appflow/gmsflow-server/server-ip/synchronize-logs'
        self.url8 = 'api/sonicos/appflow/gmsflow-server/server-ip/test-connectivity'

        self.url9 = 'api/sonicos/appflow/gmsflow-server/server-2-ip/synchronize'
        self.url10 = 'api/sonicos/appflow/gmsflow-server/server-2-ip/synchronize-logs'
        self.url11 = 'api/sonicos/appflow/gmsflow-server/server-2-ip/test-connectivity'

    def add_app_serverip_synchronize(self):
        resp = self.fw.api_post(self.url)
        return resp

    def add_app_serverip_synchronize_logs(self):
        resp = self.fw.api_post(self.url1)
        return resp

    def add_app_serverip_test(self):
        resp = self.fw.api_put(self.url2)
        return resp

    def add_app_serverip2_synchronize(self):
        resp = self.fw.api_post(self.url3)
        return resp

    def add_app_serverip2_synchronize_logs(self):
        resp = self.fw.api_post(self.url4)
        return resp

    def add_app_serverip2_test(self):
        resp = self.fw.api_post(self.url5)
        return resp

    def gms_serverip_synchronize(self):
        resp = self.fw.api_post(self.url6)
        return resp

    def gms_serverip_synchronize_logs(self):
        resp = self.fw.api_post(self.url7)
        return resp

    def gms_serverip_test(self,msg=False):
        resp = self.fw.api_post(self.url8, msg)
        return resp

    def gms_serverip2_synchronize(self):
        resp = self.fw.api_post(self.url9)
        return resp

    def gms_serverip2_synchronize_logs(self):
        resp = self.fw.api_post(self.url10)
        return resp

    def gms_serverip2_test(self):
        resp = self.fw.api_post(self.url11)
        return resp

