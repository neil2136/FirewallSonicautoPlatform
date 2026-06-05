import copy
from runner.settings import logger


class IOCIPApi:
    def __init__(self, fw):
        self.fw = fw
        self.ioc_setting_url = 'api/sonicos/indicator-of-compromise/base'
        self.ioc_enforced_file_url = 'api/sonicos/indicator-of-compromise/files'
        self.block_file_json = {
            "indicator_of_compromise": {
                "block": {
                    "file": []
                }
            }
        }

    def get_ioc_setting(self):
        # """
        # Get the general setting of IOC IP
        # returns: dict of IOC IP settings, find the detail info in edit_ioc_setting
        # """
        return self.fw.api_get(self.ioc_setting_url)

    def edit_ioc_setting(self, msg=False, **kwargs):
        # """
        # Edit IOC IP settings
        #
        # kwargs:
        #   connections_enable: bool - enable/disable IOC IP blocking for connections
        #   connections_mode: str ('all', 'firewall-rule-based') - blocking mode for connections
        #   logging: bool - enable/disable logging for IOC IP
        #   block_page: bool - enable/disable block page
        #   exclude: dict {'group': str} (AG) or {'name': str} (AO) - exclude address object/group from IOC IP blocking
        #   include_block_details: bool
        #   alert_text: str - custom alert text
        #   logo_icon: str, started with 'data:image/png;base64,...' - base64 encoded image data for logo icon
        # """
        try:
            json_input = self.get_ioc_setting()
            if 'connections_enable' in kwargs.keys():
                json_input['indicator_of_compromise']['block']['connections']['enable'] = kwargs['connections_enable']   
            if 'connections_mode' in kwargs.keys():
                json_input['indicator_of_compromise']['block']['connections']['mode'] = kwargs['connections_mode']
            if 'logging' in kwargs.keys():
                json_input['indicator_of_compromise']['logging'] = kwargs['logging']
            if 'block_page' in kwargs.keys():
                json_input['indicator_of_compromise']['block_page'] = kwargs['block_page']
            if 'exclude' in kwargs.keys():
                json_input['indicator_of_compromise']['exclude'] = kwargs['exclude']
            if 'include_block_details' in kwargs.keys():
                json_input['indicator_of_compromise']['include']['block_details'] = kwargs['include_block_details']
            if 'alert_text' in kwargs.keys():
                json_input['indicator_of_compromise']['alert_text'] = kwargs['alert_text']
            if 'logo_icon' in kwargs.keys():
                json_input['indicator_of_compromise']['logo_icon']['data'] = kwargs['logo_icon']
        except KeyError:
            logger.error("Error in creating JSON for editing ioc setting")
        logger.info(f'json_input: {json_input}')
        return self.fw.api_put(self.ioc_setting_url, msg=msg, data=json_input)

    def get_settings_file(self):
        # """
        # Get the IOC IP enforced block file list
        # returns: dict object of IOC IP enforced block file list
        # example:
        # {
        #   "indicator_of_compromise": {
        #       "block": {
        #           "file": [
        #               {"name": "file1.txt"},
        #               {"name": "file2.txt"}
        #           ]
        #       }
        #   }
        # }
        # """
        return self.fw.api_get(self.ioc_enforced_file_url)
    
    def edit_enforced_file(self, file_name=[], msg=False):
        # """
        # Edit IOC IP enforced block file list
        #
        # args:
        #   file_name: list of str - list of file names to be enforced for blocking
        #   msg: bool - whether to display messages
        # """
        if not file_name:
            logger.warning("No file name provided")
            return False
        try:
            json_input = copy.deepcopy(self.block_file_json)
            json_input['indicator_of_compromise']['block']['file'] = [{'name': fname} for fname in file_name]
        except KeyError:
            logger.error("Error in creating JSON for editing enforced file list")
        logger.info(f'json_input: {json_input}')
        return self.fw.api_put(self.ioc_enforced_file_url, msg=msg, data=json_input)
    
    def delete_enforced_files(self, msg=False):
        # """
        # Delete all the IOC IP enforced block files
        json_input = self.get_settings_file()
        logger.info(f'json_input: {json_input}')
        return self.fw.api_delete(self.ioc_enforced_file_url, msg=msg, data=json_input)



class IocIPExternalFilesApi:
    def __init__(self, fw):
        self.fw = fw
        self.external_files_url = 'api/sonicos/indicator-of-compromise-groups'
        self.external_files_statistics_url = 'api/sonicos/reporting/indicator-of-compromise-group/name/'
        self.download_file_url = 'api/sonicos/indicator-of-compromise-group/download/name/'
        self.edit_file_url = 'api/sonicos/indicator-of-compromise-groups/name/'
        
        self.http_file_json = {
            "indicator_of_compromise_groups": [
                {
                    "name": "httpioc",
                    "periodic_download": {},
                    "protocol": "https",
                    "type": {
                        "ip": True
                    },
                    "url": ""
                }
            ]
        }
        self.ftp_file_json = {
            "indicator_of_compromise_groups": [
                {
                    "directory": "/tmp/ftp_dir/",
                    "filename": "urllist.txt",
                    "login": "ftp1",
                    "name": "ftp",
                    "password": "",
                    "periodic_download": {},
                    "protocol": "ftp",
                    "server": {
                        "value": "192.168.168.10"
                    },
                    "type": {
                        "ip": True
                    }
                }
            ]
        }
        
    def get_external_files(self, msg=False):
        # """
        # Get all the info of IoC external files
        # returns: dict of IoC external files, including various details
        # example:
        # {
        #   "indicator_of_compromise_groups": [
        #       {
        #           "name": "httpioc",
        #           *some other info of this IoC file*
        #       },
        #       {
        #           "name": "ftpioc",
        #           *some other info of this IoC file*
        #       }
        #    ] 
        # }
        # """
        return self.fw.api_get(self.external_files_url)
        
    def get_external_file_by_name(self, msg=False, search_name=""):
        # """
        # Get the info of IoC external file by name
        #
        # args:
        #   search_name: str - name of the external file to search
        # returns: dict of IoC external file info if found, else None
        # """
        if not search_name:
            logger.warning("No IoC IP external file name provided for search")
            return None
        try:
            data = self.get_external_files()
            for data_info in data['indicator_of_compromise_groups']:
                if data_info['name'] == search_name:
                    return data_info
            else:
                logger.warning(f'No external file found with name: {search_name}')
                return None
        except KeyError:
            logger.error("Error in getting external file by name")
            return None
        
    def get_external_file_statistics_info_by_name(self, msg=False, file_name=""):
        # """
        # Get the statistics info of IoC external file by name
        #
        # args:
        #   file_name: str - name of the external file to get statistics
        # returns: dict of IoC external file statistics info if found
        # """
        if not file_name:
            logger.warning("No file name provided for getting statistics")
            return None
        url = self.external_files_statistics_url + file_name
        logger.info(f"Getting IoC external file statistics: {file_name} from URL: {url}")
        return self.fw.api_get(url)

    def add_http_file(self, msg=False, **kwargs):
        # """
        # Add an IoC external file using HTTP/S protocol
        #
        # kwargs:
        #   name: str - name of the external file, the name should be unique
        #   url: str - URL of the external file, should be started with http:// or https://
        #   periodic_download: dict - periodic download settings
        #   -- to disable periodic download, set it to {}
        #   -- to enable periodic download, set it to: {"interval": str}, the str can be one of: 
        #   --- ["5-minutes", "15-minutes", "1-hour", "24-hours"]
        # """
        try:
            json_input = copy.deepcopy(self.http_file_json)
            if 'name' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['name'] = kwargs['name']
            if 'url' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['url'] = kwargs['url']
            if 'periodic_download' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['periodic_download'] = kwargs['periodic_download']
        except KeyError:
            logger.error("Error in creating JSON for adding HTTP IoC external file")
        logger.info(f'json_input: {json_input}')
        return self.fw.api_post(self.external_files_url, msg=msg, data=json_input)

    def add_ftp_file(self, msg=False, **kwargs):
        # """
        # Add an IoC external file using FTP protocol
        #
        # kwargs:
        #   name: str - name of the external file, the name should be unique
        #   server: dict - a dict contains FTP server address, e.x: {"value": "10.20.30.40"}
        #   directory: str - directory path on the FTP server
        #   filename: str - filename on the FTP server
        #   login: str - FTP login username
        #   password: str - FTP login password
        #   periodic_download: dict - periodic download settings, see add_http_file for details
        # """
        try:
            json_input = self.ftp_file_json.copy()
            if 'name' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['name'] = kwargs['name']
            if 'directory' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['directory'] = kwargs['directory']
            if 'filename' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['filename'] = kwargs['filename']
            if 'login' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['login'] = kwargs['login']
            if 'password' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['password'] = kwargs['password']
            if 'server' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['server'] = kwargs['server']
            if 'periodic_download' in kwargs:
                json_input['indicator_of_compromise_groups'][0]['periodic_download'] = kwargs['periodic_download']
        except KeyError:
            logger.error("Error in creating JSON for adding FTP IoC external file")
        logger.info(f'json_input: {json_input}')
        return self.fw.api_post(self.external_files_url, msg=msg, data=json_input)

    def modify_external_file_by_name(self, msg=False, file_name="", **kwargs):
        # Modify an IoC external file by its name. use self.get_external_file_by_name get base configuration
        #  kwargs example:
        # {
        #     'name': 'host_12.12.1.40', 
        #     'type': {'ip': True}, 
        #     'periodic_download': {}, 
        #     'protocol': 'https', 
        #     'url': 'https://192.168.168.10/host_12.12.1.40.txt'
        # }
        if not file_name:
            logger.warning("No file name provided for modification")
            return False if not msg else (False, "No file name provided for modification")
        url = self.edit_file_url + file_name
        logger.info(f"Modifying IoC file: {file_name} from URL: {url}")
        json_input = {"indicator_of_compromise_groups": []}
        json_input['indicator_of_compromise_groups'].append(self.get_external_file_by_name(search_name=file_name))
        logger.info(f"Current external file configuration: {json_input}")
        if 'name' in kwargs:
            json_input["indicator_of_compromise_groups"][0]['name'] = kwargs['name']
        if 'type' in kwargs:
            json_input["indicator_of_compromise_groups"][0]['type'] = kwargs['type']
        if 'periodic_download' in kwargs:
            json_input["indicator_of_compromise_groups"][0]['periodic_download'] = kwargs['periodic_download']
        if 'protocol' in kwargs:
            if kwargs['protocol'] == 'https':
                json_input["indicator_of_compromise_groups"][0]['protocol'] = 'https'
                if 'url' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['url'] = kwargs['url']
            elif kwargs['protocol'] == 'ftp':
                json_input["indicator_of_compromise_groups"][0]['protocol'] = 'ftp'
                if 'server' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['server'] = kwargs["server"]
                if 'login' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['login'] = kwargs["login"]
                if 'password' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['password'] = kwargs["password"]
                if 'directory' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['directory'] = kwargs["directory"]
                if 'filename' in kwargs:
                    json_input["indicator_of_compromise_groups"][0]['filename'] = kwargs["filename"]
                    
        logger.info(f'Modified external file configuration result: {json_input}')
        return self.fw.api_put(url, msg=msg, data=json_input)
    
    def download_external_file_by_name(self, msg=False, file_name=""):
        # """
        # Download the IoC external file by name
        # args:
        #   file_name: str - name of the external file to download
        # """
        if not file_name:
            logger.warning("No file name provided for download")
            return False
        url = self.download_file_url + file_name
        logger.info(f"Downloading IoC file: {file_name} from URL: {url}")
        return self.fw.api_post(url, msg=msg, data={})
    
    def delete_external_file_by_name(self, msg=False, file_name=""):
        # """
        # Delete the IoC external file by name
        # args:
        #   file_name: str - name of the external file to delete
        # """
        if not file_name:
            logger.warning("No file name provided for deletion")
            return False
        url = self.external_files_url + '/name/' + file_name
        logger.info(f"Deleting IoC external file: {file_name} from URL: {url}")
        return self.fw.api_delete(url)
    
    def delete_external_files(self, msg=False):
        # """
        # Delete all the IoC external files
        res = False
        try: 
            del_namelist = []
            namelist_raw_data = self.get_external_files()
            for file_name in namelist_raw_data.get('indicator_of_compromise_groups', []):
                del_namelist.append(file_name.get('name'))
            logger.info(f"Deleting all IoC external files: {del_namelist}")
            for del_name in del_namelist:
                del_res = self.delete_external_file_by_name(msg=msg, file_name=del_name)
                if not del_res:
                    logger.error(f"Failed to delete IoC external file: {del_name}")
                    break
            else:
                res = True
        except Exception as e:
            logger.error(f"Exception occurred while deleting IoC external files: {e}")
        return res
    
    def get_external_file_ip_list_by_name(self, msg=False, file_name=""):
        # """
        # Get the IoC external file IP list by name
        # args:
        #   file_name: str - name of the external file to get IP list
        # returns: dict with keys "ip_list" (list of IP ranges and type) and "count" (number of IP ranges)
        # """
        if not file_name:
            logger.warning("No file name provided for download")
            return None
        url = f'api/sonicos/dynamic-file/getIOCGroupRTIPList.json?groupName={file_name}&type=1'
        # Example response:
        #"IOCGroupRTIPList": "iocGroupRTIPAddr1,iocGroupRTIPAddr2,type|10.177.0.0,10.177.255.255,1|3.7.8.1,3.7.8.1,0",
        #"IOCGroupRTIPListCount": "3",
        #"systime": 1767924505,
        #"loggedin": true
        try:
            out = self.fw.api_get(url)
            
            data = {
                "ip_list": [],
                "count": int(out.get("IOCGroupRTIPListCount", 0))
            }
            
            original_list = out.get("IOCGroupRTIPList", "")
            if not original_list:
                logger.error("Incorrect response received")
                return None
            elif "|" not in original_list:
                if data["count"] == 0 and out.get("IOCGroupRTIPList", "") == "iocGroupRTIPAddr1,iocGroupRTIPAddr2,type":
                    logger.debug("empty IP list received")
                    return data
                else:
                    logger.error("Incorrect response received")
                    return None
            else:
                entries = original_list.split("|")
                for entry in entries:
                    ip_range_type = entry.split(",")
                    if len(ip_range_type) != 3:
                        logger.error(f"Unexpected entry format: {entry}")
                        continue
                    if ip_range_type[2] == "type":
                        # skip header
                        continue
                    data["ip_list"].append([ip_range_type[0], ip_range_type[1], int(ip_range_type[2])])
                return data
        except Exception as e:
            logger.error(f"Failed to get file IP list: {e}")
            return None


class IOCDiagnosticsApi:
    def __init__(self, fw):
        self.fw = fw
        self.ioc_lookup_url = 'api/sonicos/diag/ioc-lookup/'
        self.ioc_stats_url = 'api/sonicos/dynamic-file/getIOCStats.json'

    def check_ioc_lookup(self, msg=False, ip=''):
        url = self.ioc_lookup_url + ip
        return self.fw.api_post(url, msg=msg, data={})

    def get_ip_statistics(self):
        return self.fw.api_get(self.ioc_stats_url)

