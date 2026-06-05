from runner.settings import logger
from runner.utils.assertion import Assertion
from pprint import pprint
import copy

class ApplicationApi:
    '''ApplicationApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/application-groups'

    def get_application_group(self, name=None, uuid=None):
        if name:
            get_url = self.url + '/name/' + name
            out = self.fw.api_get(get_url)
            return out

        if uuid:
            get_url = self.url + '/uuid/' + uuid
            out = self.fw.api_get(get_url)
            return out

        else:
            out = self.fw.api_get(self.url)
            return out
        return out

    def add_application_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        application_resp = self.fw.api_post(self.url, msg, data=json_input)
        return application_resp

    def del_application_group(self, name):
        url = self.url + '/name/' + name
        application_resp = self.fw.api_delete(url)
        return application_resp

    def edit_application_group(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp
    def edit_application_group_using_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url + '/uuid/' + uuid
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp
     
    def delete_application_group_using_uuid(self, uuid):
        if uuid:
            url = self.url + '/uuid/' + uuid
        else:
            logger.error('either name or uuid shoule be specified for delete_application_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp

class ScheduleObjectApi:
    '''ScheduleObjectApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/schedules'

    def get_schedule_object(self):
        out = self.fw.api_get(self.url)
        return out


    def add_schedule_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        schedule_resp = self.fw.api_post(self.url, msg, data=json_input)
        return schedule_resp

    def edit_schedule_object(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp
    
    def delete_schedule_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_delete(self.url, msg, data=json_input)
        return resp


class DynamicGroupApi:
    '''DynamicGroupApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dynamic-external-objects'
        self.reporting_url = 'api/sonicos/reporting/dynamic-external-objects'
        self.download_url = 'api/sonicos/dynamic-external-object/download/name/'
        self.getObject_url = 'api/sonicos/dynamic-file/getObjectList.json?type=1'

        self.initial_dynamic_external_group_json = {
            "dynamic_external_objects":
                [
                   {
                       "name":"",
                       "type":{"address_group":True},
                       "zone":"LAN",
                       "fqdn":False,
                       "periodic_download":{},#"5-minutes","15-minutes","1-hour","24-hours"
                       "protocol":"https",# https , ftp
                   }
                ]
            }

    def build_json_dynamic_external_group(self, **kwargs):
        #kwargs example：
        # ftp_base_dict = {
        #     "name": "",
        #     "periodic_download": "5-minutes",
        #     "protocol": "ftp",
        #     "fqdn":False,
        #     "server":Parameter.SERVER,
        #     "login":"kelly",
        #     "password":"password",
        #     "directory":"/var/ftp/ForEDAG",
        #     "filename":""}
        #
        # https_base_dict = {
        #     "name": "",
        #     "protocol": "https",
        #     "url": ""
        # }
        json_input = copy.deepcopy(self.initial_dynamic_external_group_json)
        path = json_input['dynamic_external_objects'][0]
        try:
            if 'name' in kwargs.keys() and kwargs['name']:
                path['name'] = kwargs['name']
            else:
                logger.info('Please input Dynamic Group name')
                return False
            if 'fqdn' in kwargs.keys() and kwargs['fqdn']:
                path['fqdn'] = kwargs['fqdn']
            if 'zone' in kwargs.keys() and kwargs['zone']:
                path['zone'] = kwargs['zone']
            if 'periodic_download' in kwargs.keys() and kwargs['periodic_download']:
                path['periodic_download']={}
                path['periodic_download']['interval'] = kwargs['periodic_download']
            if 'protocol' in kwargs.keys() and kwargs['protocol']:
                path['protocol'] = kwargs['protocol']
                if kwargs['protocol'] == 'https':
                    path['url'] = kwargs['url']
                elif kwargs['protocol'] == 'ftp':

                    path['login'] = kwargs['login']
                    path['password'] = kwargs['password']
                    path['directory'] = kwargs['directory']
                    path['filename'] = kwargs['filename']
                    path['server'] = {}
                    path['server']['value'] = kwargs['server']
                else:
                    logger.info('Please input correct protocol')
                    return False
        except KeyError:
            logger.info("Error: In creating JSON for dynamic_external_group")
        logger.info(json_input)
        return json_input

    def get_dynamic_group(self):
        out = self.fw.api_get(self.url)
        return out

    def add_dynamic_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        dynamic_resp = self.fw.api_post(self.url, msg, data=json_input)
        return dynamic_resp

    def edit_dynamic_group(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_group + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def add_dynamic_group_by_build_json(self, msg=False, **kwargs):
        json_input = self.build_json_dynamic_external_group(**kwargs)
        if not json_input:
            return False if not msg else (False, dict)
        logger.info(json_input)
        logger.info(f'add_dynamic_group post url: {self.url}')
        return self.fw.api_post(self.url, msg, data=json_input)

    def get_dynamic_group_json(self, name: str):
        jsonurl = 'api/sonicos/dynamic-file/getDynGroupRTIPList.json?groupName=' + name + '&type=2'
        logger.info(f'get_dynamic_group_json get url: {jsonurl}')
        return self.fw.api_get(jsonurl)

    def edit_dynamic_group_by_name(self, msg=False, **kwargs):
        json_input = self.build_json_dynamic_external_group(**kwargs)
        if not json_input:
            return False if not msg else (False, dict)
        edit_url = self.url + '/name/' + kwargs['name']
        logger.info(f'edit_dynamic_group_json put url: {edit_url}')
        logger.info(json_input)
        return self.fw.api_put(edit_url, msg, data=json_input)

    def download_dynamic_group(self, name: str, msg=False):
        if not name:
            logger.info("please enter dynamic group name")
            return False if not msg else (False, dict)
        download_name_url = self.download_url + name
        logger.info(f'download_dynamic_group post url: {download_name_url}')
        return self.fw.api_post(download_name_url, msg)

    def delete_dynamic_group(self, name: str, msg=False):
        if not name:
            logger.info("please enter dynamic group name")
            return False if not msg else (False, dict)
        delete_url = self.url+ '/name/' + name
        logger.info(f'delete_dynamic_group delete url: {delete_url}')
        return self.fw.api_delete(delete_url, msg)

    def delete_multiple_dynamic_group(self, *name_list, msg=False):
        json_input = {"dynamic_external_objects":[]}
        for name in name_list:
            json_input['dynamic_external_objects'].append({'name':name})
        logger.info(json_input)
        logger.info(f'delete_multiple_dynamic_group delete url: {self.url}')
        return self.fw.api_delete(self.url, msg, data=json_input)

    def flush_dynamic_group(self, name: str, msg=False):
        if not name:
            logger.info("please enter dynamic group name")
            return False if not msg else (False, dict)
        flush_url = self.reporting_url  + '/name/' + name
        logger.info(f'flush_dynamic_group delete url: {flush_url}')
        return self.fw.api_delete(flush_url, msg)

    def statistics_dynamic_group(self, name: str):
        statistics_url = self.reporting_url  + '/name/' + name
        logger.info(f'statistics_dynamic_group get url: {statistics_url}')
        return self.fw.api_get(statistics_url)

    def get_addr_obj_list(self):
        logger.info(f'getObjectList get url: {self.getObject_url}')
        ObjectList = self.fw.api_get(self.getObject_url)
        if isinstance(ObjectList, dict) and "addrObjArray" in ObjectList.keys():
            return ObjectList["addrObjArray"]
        else:
            return ''

class SecurityActionProfilesApi:
    '''Security Action Profiles class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/security-action-profiles'
        self.url_name = 'api/sonicos/security-action-profiles/name'

    def get_security_action_profiles(self):
        out = self.fw.api_get(self.url)
        return out

    def get_security_action_profile_use_name(self, file_name):
        url_file_name = str(self.url_name + '/' + file_name)
        logger.info(url_file_name)
        out = self.fw.api_get(url_file_name)
        return out

    def add_security_action_profiles(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_post(self.url, msg, data=json_input)
        return res

    def edit_security_action_profiles(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(self.url, msg, data=json_input)
        return res
        
    def edit_security_action_profiles_by_name(self,name, msg=False, **kwargs):
        if not name:
            logger.info('pls enter security action profile name')
        else:
            url = self.url_name + '/' + name
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def patch_security_action_profiles(self):
        pass

    def get_security_action_profile_name(self, name):
        url = self.url + '/name/' + str(name)
        out = self.fw.api_get(url)
        return out

    def edit_security_action_profile_name(self, msg=False, name='', **kwargs):
        if name == '' and 'name' not in kwargs.keys():
            logger.error('Please pass in a profile name.')
            return False

        url = self.url + '/name/'
        if name == '':
            url = url + str(kwargs['name'])
        else:
            url = url + str(name)

        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res
    
    def edit_security_action_profiles_by_name(self,name, msg=False, **kwargs):
        if not name:
            logger.info('pls enter security action profile name')
        else:
            url = self.url_name + '/' + name
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_security_action_profile_name(self, name):
        url = self.url + '/name/' + str(name)
        res = self.fw.api_delete(url)
        return res

    def get_security_action_profile_uuid(self, uuid):
        url = self.url + '/uuid/' + str(uuid)
        out = self.fw.api_get(url)
        return out

    def edit_security_action_profile_uuid(self, msg=False, uuid='', **kwargs):
        if uuid == '' and 'uuid' not in kwargs.keys():
            logger.error('Please pass in a profile uuid.')
            return False

        url = self.url + '/uuid/'
        if uuid == '':
            url = url + str(kwargs['uuid'])
        else:
            url = url + str(uuid)

        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_security_action_profile_uuid(self, uuid):
        url = self.url + '/uuid/' + str(uuid)
        res = self.fw.api_delete(url)
        return res


class DosActionProfilesApi:
    '''Dos Action Profiles class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dos-action-profiles'
        self.url_name = 'api/sonicos/dos-action-profiles/name/'
        self.url_uuid = 'api/sonicos/dos-action-profiles/uuid/'

    def get_dos_action_profiles(self):
        out = self.fw.api_get(self.url)
        return out

    def get_dos_action_profile_by_name(self, name):
        url = self.url_name + str(name)
        out = self.fw.api_get(url)
        return out

    def get_dos_action_profile_by_uuid(self, uuid):
        url = self.url_uuid + str(uuid)
        out = self.fw.api_get(url)
        return out

    def add_dos_action_profiles(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_post(self.url, msg, data=json_input)
        return res    

    def edit_dos_action_profile_by_name(self, msg=False, name='', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if name == '' and 'name' not in kwargs.keys():
            logger.error('Please pass in a profile name.')
            return False
        if name == '':
            url = self.url_name + str(kwargs['name'])
        else:
            url = self.url_name + str(name)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def edit_dos_action_profile_by_uuid(self, msg=False, uuid='', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if uuid == '' and 'uuid' not in kwargs.keys():
            logger.error('Please pass in a profile uuid.')
            return False
        if uuid == '':
            url = self.url_uuid + str(kwargs['uuid'])
        else:
            url = self.url_uuid + str(uuid)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_dos_action_profile_by_name(self, name):
        url = self.url_name + str(name)
        res = self.fw.api_delete(url)
        return res    

    def del_dos_action_profile_by_uuid(self, uuid):
        url = self.url_uuid + str(uuid)
        res = self.fw.api_delete(url)
        return res

    def add_dos_action_profiles_login_false(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_post(self.url, msg, nologin=True, data=json_input)
        return res


    def del_dos_action_profile_by_name_login_false(self, name):
        url = self.url_name + str(name)
        res = self.fw.api_delete(url, nologin=True)
        return res

    def del_dos_action_profile_by_uuid_login_false(self, uuid):
        url = self.url_uuid + str(uuid)
        res = self.fw.api_delete(url, nologin=True)
        return res
        

class WebCategoryApi:
    '''WebCategoryApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/web-category-groups'

    def add_web_category(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def get_web_category(self,name=None):
        if name:
            url = self.url + '/name/'+name
        else:
            url = self.url
        resp = self.fw.api_get(url)
        return resp

    def edit_web_category_by_name(self, msg=False, name='', **kwargs):
        if name == '' and 'name' not in kwargs.keys():
            logger.error('Please pass in a profile name.')
            return False

        url = self.url + '/name/'
        if name == '':
            url = url + str(kwargs['name'])
        else:
            url = url + str(name)

        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_web_category(self,name):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name shoule be specified for delete web_category.')
            return False
        resp = self.fw.api_delete(url)
        return resp


class UriListApi:
    '''UriListApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/uri-list-objects'

    def add_uri_list_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def get_uri_list_object(self, name=None):
        if name:
            url = self.url + '/name/'+name
        else:
            url = self.url
        resp = self.fw.api_get(url)
        return resp

    def edit_uri_list_object_by_name(self, msg=False, name='', **kwargs):
        if name == '' and 'name' not in kwargs.keys():
            logger.error('Please pass in a uri list object name.')
            return False

        url = self.url + '/name/'
        if name == '':
            url = url + str(kwargs['name'])
        else:
            url = url + str(name)

        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_uri_list_object(self, name):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name shoule be specified for delete uri list object.')
            return False
        resp = self.fw.api_delete(url)
        return resp


class UriGroupApi:
    '''UriGroupApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/uri-list-groups'

    def add_uri_list_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def get_uri_list_group(self, name=None):
        if name:
            url = self.url + '/name/'+name
        else:
            url = self.url
        resp = self.fw.api_get(url)
        return resp

    def edit_uri_list_group_by_name(self, msg=False, name='', **kwargs):
        if name == '' and 'name' not in kwargs.keys():
            logger.error('Please pass in a uri group name.')
            return False

        url = self.url + '/name/'
        if name == '':
            url = url + str(kwargs['name'])
        else:
            url = url + str(name)

        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    def del_uri_list_group(self, **kwargs):
        input_json = copy.deepcopy(kwargs)
        resp = self.fw.api_delete(self.url, data=input_json)
        return resp


class WebsitesApi:
    '''WebsitesApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_object = 'api/sonicos/website-objects'
        self.url_group = 'api/sonicos/website-groups'

    def get_websites_object(self):
        out = self.fw.api_get(self.url_object)
        return out

    def get_websites_object_by_name(self, name):
        url = self.url_object + '/' + 'name' + '/' + name
        logger.info(url)
        out = self.fw.api_get(url)
        return out

    def get_websites_object_by_uuid(self, uuid):
        url = self.url_object + '/' + 'uuid' + '/' + uuid
        logger.info(url)
        out = self.fw.api_get(url)
        return out

    def add_websites_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url_object, msg, data=json_input)
        return resp

    def edit_websites_object(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_object + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def edit_websites_object_by_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        uuid_url = self.url_object + '/uuid/' + uuid
        resp = self.fw.api_put(uuid_url, msg, data=json_input)
        return resp

    def del_websites_object(self, name):
        if name:
            url = self.url_object + '/name/' + name
        else:
            logger.error('name should be specified to delete websites_object.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_websites_object_by_uuid(self, uuid):
        if uuid:
            url = self.url_object + '/uuid/' + uuid
        else:
            logger.error('UUID should be specified to delete websites_object.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def get_websites_group(self):
        out = self.fw.api_get(self.url_group)
        return out

    def get_websites_group_by_name(self, name):
        url = self.url_group + '/' + 'name' + '/' + name
        logger.info(url)
        out = self.fw.api_get(url)
        return out

    def get_websites_group_by_uuid(self, uuid):
        url = self.url_group + '/' + 'uuid' + '/' + uuid
        logger.info(url)
        out = self.fw.api_get(url)
        return out

    def add_websites_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url_group, msg, data=json_input)
        return resp

    def edit_websites_group(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_group + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def edit_websites_group_by_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        uuid_url = self.url_group + '/uuid/' + uuid
        resp = self.fw.api_put(uuid_url, msg, data=json_input)
        return resp

    def del_websites_group(self, name):
        if name:
            url = self.url_group + '/name/' + name
        else:
            logger.error('name should be specified to delete websites_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_websites_group_by_uuid(self, uuid):
        if uuid:
            url = self.url_group + '/uuid/' + uuid
        else:
            logger.error('UUID should be specified to delete websites_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp


class CountryApi:
    '''CountryApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url_group = 'api/sonicos/country-groups'

    def get_country_group(self, name=None, uuid=None):
        if name:
            edit_url = self.url_group + '/name/' + name
            out = self.fw.api_get(edit_url)
            return out

        if uuid:
            edit_url = self.url_group + '/uuid/' + uuid
            out = self.fw.api_get(edit_url)
            return out

        else:
            out = self.fw.api_get(self.url_group)
            return out

    def add_country_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url_group, msg, data=json_input)
        return resp

    def edit_country_group(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_group + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def edit_country_group_using_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_group + '/uuid/' + uuid
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def del_country_group(self,name):
        if name:
            url = self.url_group + '/name/' + name
        else:
            logger.error('name shoule be specified for delete country_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_multiple_country_group(self,msg=False,**kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_delete(self.url_group, msg, data=json_input)
        return resp

    def del_country_group_using_uuid(self, uuid):
        if uuid:
            url = self.url_group + '/uuid/' + uuid
        else:
            logger.error('either name or uuid shoule be specified for delete country_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp



class ThreatPreventionProfilesApi:
    '''ThreatPreventionProfilesApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/threat-prevention-profiles'

    def get_threat_prevention_profile(self, name=None):
        if name:
            url = self.url + '/name/' + name
        else:
            url = self.url
        out = self.fw.api_get(url)
        return out

    def add_threat_prevention_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def del_threat_prevention_profile(self, name):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name should be specified for delete threat_prevention_profile.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def edit_threat_prevention_profile_by_uuid(self, name, msg=False, **kwargs):
        if not name:
            logger.info('pls enter profile name')
            return False
        else:
            logger.info('Get profile uuid')
            data = self.fw.api_get(self.url)
            profile_uuid = None
            for profile in data['threat_prevention_profiles']:
                if profile['name'] == name:
                    profile_uuid = profile['uuid']
                    logger.info('The UUID of ' + name + ' is: ' + profile_uuid)
                    break
            url_edit = self.url + '/uuid/' + profile_uuid
            json_input = copy.deepcopy(kwargs)
            resp = self.fw.api_put(url_edit, msg, data=json_input)
            return resp
            

class AddressObjectGroupApi:
    '''AddressObjectGroupApi'''
    def __init__(self,fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/address-groups/ipv4/'
        self.url_v6 = 'api/sonicos/address-groups/ipv6/'

    def add_addressgroup(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        if 'ipv6' in kwargs['address_groups'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_addressgroup(self, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        return resp
        
    def get_addressgroup_by_name(self, name: str, version = 'v4'):
        if version == 'v4':
            url = self.url_v4 +  'name/' + name
        else:
            url = self.url_v6 + 'name/' + name
        resp = self.fw.api_get(url)
        logger.info(f'get_addressgroup_by_name get url: {url}')
        return resp
    
    def edit_addressgroup(self, version = 'v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        if version == 'v4':
            url_edit = self.url_v4
        else:
            url_edit = self.url_v6
        resp = self.fw.api_put(url_edit, data=json_input)
        return resp

    # because edit_addressgroup can not support add name to api url
    def edit_addressgroup_by_name(self, version='v4', name='', msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        if version == 'v4':
            url_edit = self.url_v4
        else:
            url_edit = self.url_v6
        if name is '':
            logger.error('key parameter: name do not empty.')
            return (False, {}) if msg else False
        resp = self.fw.api_put(url_edit+'name/'+name, msg, data=json_input)
        return resp

    def del_addressgroup(self, name, version = 'v4', msg=False):
        if version == 'v4':
            url = self.url_v4
        else:
            url = self.url_v6
        if name:
            url = url + 'name/' + name
        else:
            logger.error('name should be specified for delete address object group.')
            return False
        resp = self.fw.api_delete(url, msg)
        return resp


class CustomMatchApi:
    '''CustomMatchApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.custom_match_object = 'api/sonicos/custom-matches'
        self.custom_match_group = 'api/sonicos/custom-match-groups'

    def get_custom_match_object(self):
        resp = self.fw.api_get(self.custom_match_object)
        return resp

    def add_custom_match_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.custom_match_object, msg, data=json_input)
        return resp

    def edit_custom_match_object(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.custom_match_object + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def del_custom_match_object_name(self, name):
        if name:
            url = self.custom_match_object + '/name/' + name
        else:
            logger.error('name shoule be specified for delete custom match _object.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_custom_match_object_uuid(self, uuid):
        url = self.custom_match_object + '/uuid/' + str(uuid)
        res = self.fw.api_delete(url)
        return res

    def get_custom_match_group(self):
        resp = self.fw.api_get(self.custom_match_group)
        return resp

    def add_custom_match_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.custom_match_group, msg, data=json_input)
        return resp

    def edit_custom_match_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.custom_match_group, msg, data=json_input)
        return resp

    def edit_custom_match_group_name(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.custom_match_group + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def del_custom_match_group_name(self, name):
        if name:
            url = self.custom_match_group + '/name/' + name
        else:
            logger.error('name shoule be specified for delete custom match_group.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_custom_match_group_uuid(self, uuid):
        url = self.custom_match_group + '/uuid/' + str(uuid)
        res = self.fw.api_delete(url)
        return res

class MatchPatternApi:
    '''CustomMatchApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/match-objects'

    def get_match_pattern_by_name(self, name):
        url = self.url + '/name/' + name
        get_response = self.fw.api_get(url)
        return get_response

    def add_match_pattern(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def edit_match_pattern(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def del_match_pattern_name(self, name):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name shoule be specified for delete custom match _object.')
            return False
        resp = self.fw.api_delete(url)
        return resp

class ReportingProfilesApi:
    '''ReportingProfilesApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_base = 'api/sonicos/reporting-profiles'
        self.url_config = 'api/sonicos/reporting-profiles/name/'

        self.initial_repo_profile_json = {
            "reporting_profiles": [{
                "name": "",
		        "uuid": "",
		        "frequency": 0,
		        "log_monitor": False,
		        "email_alert": False,
		        "email_address": "",
		        "syslog": False,
		        "syslog_profile": 0,
		        "ipfix": False,
		        "color": {
			        "hex": "0x00FF0000"
		        },
		        "event": {
			        "matched": False,
			        "begin": False,
			        "end": False
		        }
            }]
        }

    def get_reporting_profile(self):
        output = self.fw.api_get(self.url_base)
        return output

    def add_reporting_profile(self, msg=False, **kwargs):
        try:
            json_input = self.build_json_repo_profile(**kwargs)
            logger.info("\n\nUpdate Json is :\n")
            pprint(json_input)
        except KeyError:
            logger.info("Error in creating JSON for reporting profile")

        resp = self.fw.api_post(self.url_base, msg, data=json_input)
        return resp

    def edit_reporting_profile(self, msg=False, **kwargs):
        url_edit = str(self.url_config + kwargs['old_profile_name'])
        logger.info(url_edit)
        try:
            json_input = self.build_json_repo_profile(**kwargs)
            logger.info("\n\nUpdate Json is :\n")
            pprint(json_input)
        except KeyError:
            logger.info("Error in creating JSON for reporting profile")

        resp = self.fw.api_put(url_edit, msg, data=json_input)
        return resp

    def del_reporting_profile(self, profile_name):
        url_del = str(self.url_config + profile_name)
        logger.info(url_del)
        res = self.fw.api_delete(url_del)
        return res

    def patch_reporting_profile(self):
        pass

    def build_json_repo_profile(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_repo_profile_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        if 'profile_name' in kwargs.keys() and kwargs['profile_name']:
            json_input['reporting_profiles'][0]['name'] = kwargs['profile_name']
        else:
            logger.info('Please input profile name')
            return False
        if 'uuid' in kwargs.keys() and kwargs['uuid']: 
            json_input['reporting_profiles'][0]['uuid'] = kwargs['uuid']
        if 'frequency' in kwargs.keys() and kwargs['frequency']:
            json_input['reporting_profiles'][0]['frequency'] = kwargs['frequency']
        if 'log_monitor' in kwargs.keys() and kwargs['log_monitor']:
            json_input['reporting_profiles'][0]['log_monitor'] = kwargs['log_monitor']
        if 'syslog' in kwargs.keys() and kwargs['syslog']:
            json_input['reporting_profiles'][0]['syslog'] = kwargs['syslog']
        if 'syslog_profile' in kwargs.keys() and kwargs['syslog_profile']:
            json_input['reporting_profiles'][0]['syslog_profile'] = kwargs['syslog_profile']
        if 'ipfix' in kwargs.keys() and kwargs['ipfix']:
            json_input['reporting_profiles'][0]['ipfix'] = kwargs['ipfix']
        if 'color_hex' in kwargs.keys() and kwargs['color_hex']:
            json_input['reporting_profiles'][0]['color']['hex'] = kwargs['color_hex']
        if 'email_alert' in kwargs.keys() and kwargs['email_alert']:
            json_input['reporting_profiles'][0]['email_alert'] = kwargs['email_alert']
        if 'email_address' in kwargs.keys() and kwargs['email_address']:
            json_input['reporting_profiles'][0]['email_address'] = kwargs['email_address']
        if 'event_matched' in kwargs.keys() and kwargs['event_matched']:
            json_input['reporting_profiles'][0]['event']['matched'] = kwargs['event_matched']
        if 'event_begin' in kwargs.keys() and kwargs['event_begin']:
            json_input['reporting_profiles'][0]['event']['begin'] = kwargs['event_begin']
        if 'event_end' in kwargs.keys() and kwargs['event_end']:
            json_input['reporting_profiles'][0]['event']['end'] = kwargs['event_end']

        return json_input

    def add_reporting_profile_deepcopy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        reporting_profile_resp = self.fw.api_post(self.url_base, msg, data=json_input)
        return reporting_profile_resp
        
        
class ReputationApi:
    '''ReputationApi class'''
    
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/reputation-objects'

        self.initial_repu_json = {
            "content_filter": {
                "reputation_object": [
                    {
                        "name": "CFS Default Reputation Object",
                        "uuid": "80dd516c-62b2-4290-3800-2cb8ed6d8008",
                        "ranges": "default"
                    }
                ]
            }
        }

    def get_reputations(self):
        out = self.fw.api_get(self.url)
        return out

    def get_reputation_by_name(self, name):
        url = self.url + '/name/' + name
        repu_resp = self.fw.api_get(url)
        return repu_resp

    def add_reputation(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url, msg, data=json_input)
        return repu_resp

    def edit_reputation(self, msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify reputation name')
            return False
        url_edit = self.url + '/name/' + name
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return repu_resp

    def del_reputation_by_name(self, name=None):
        if not name:
            logger.info('Please specify reputation name')
            return False
        url = self.url + '/name/' + name
        repu_resp = self.fw.api_delete(url)
        return repu_resp

    def del_reputations(self):
        repu_resp = self.fw.api_delete(self.url)
        return repu_resp
        
        
class PDFApi:

    '''PDFApi class'''
    
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/packet-dissection-objects'
        self.url_group = 'api/sonicos/packet-dissection-groups'

        self.initial_pdf_json = {
            "packet_dissection_objects": 
            [{}],
        }
        self.initial_pdf_group_json = {
            "packet_dissection_groups": 
            [{}],
        }

    def add_pdf_obj(self, msg=False, **kwargs):
        json_input = self.initial_pdf_json
        if 'name' not in kwargs.keys() or 'negative' not in kwargs.keys() or 'family' not in kwargs.keys():
            logger.error('Please specify name,negative,family,data-type when add pdf object.')
            return False
        json_input['packet_dissection_objects'][0]['name'] = kwargs['name']
        json_input['packet_dissection_objects'][0]['negative_matching'] = kwargs['negative']
        json_input['packet_dissection_objects'][0]['family'] = kwargs['family']
        if 'numeric' in kwargs['data_type'].keys():
            kwargs['data_type']['numeric']['value'] = int(kwargs['data_type']['numeric']['value'])
        elif 'ipv6_range' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv6_range']['start'] = kwargs['data_type']['ipv6_range']['start']
            kwargs['data_type']['ipv6_range']['end'] = kwargs['data_type']['ipv6_range']['end']
        elif 'range' in kwargs['data_type'].keys():
            kwargs['data_type']['range']['start'] = int(kwargs['data_type']['range']['start'])
            kwargs['data_type']['range']['end'] = int(kwargs['data_type']['range']['end'])
        elif 'tcp_bitset' in kwargs['data_type'].keys():
            kwargs['data_type']['tcp_bitset'] = kwargs['data_type']['tcp_bitset']
        elif 'ipv4_bitset' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv4_bitset'] = kwargs['data_type']['ipv4_bitset']
        elif 'ipv6_address' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv6_address'] = kwargs['data_type']['ipv6_address']
        json_input['packet_dissection_objects'][0]['data_type'] = kwargs['data_type']
        logger.info(json_input)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        logger.info(resp)
        return resp
     
    def edit_pdf_obj(self, msg=False, **kwargs):
        json_input = self.initial_pdf_json
        if 'name' not in kwargs.keys():
            logger.error('Please specify name when edit pdf object.')
            return False
        url = self.url + '/name/' + kwargs['name']
        if 'name_new' in kwargs.keys():
            json_input['packet_dissection_objects'][0]['name'] = kwargs['name_new']
        else:
            json_input['packet_dissection_objects'][0]['name'] = kwargs['name']
        if 'negative' in kwargs.keys():
            json_input['packet_dissection_objects'][0]['negative_matching'] = kwargs['negative']
        if 'family' in kwargs.keys():
            json_input['packet_dissection_objects'][0]['family'] = kwargs['family']
        if 'numeric' in kwargs['data_type'].keys():
            kwargs['data_type']['numeric']['value'] = int(kwargs['data_type']['numeric']['value'])
        elif 'ipv6_range' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv6_range']['start'] = kwargs['data_type']['ipv6_range']['start']
            kwargs['data_type']['ipv6_range']['end'] = kwargs['data_type']['ipv6_range']['end']
        elif 'range' in kwargs['data_type'].keys():
            kwargs['data_type']['range']['start'] = int(kwargs['data_type']['range']['start'])
            kwargs['data_type']['range']['end'] = int(kwargs['data_type']['range']['end'])
        elif 'tcp_bitset' in kwargs['data_type'].keys():
            kwargs['data_type']['tcp_bitset'] = kwargs['data_type']['tcp_bitset']
        elif 'ipv4_bitset' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv4_bitset'] = kwargs['data_type']['ipv4_bitset']
        elif 'ipv6_address' in kwargs['data_type'].keys():
            kwargs['data_type']['ipv6_address'] = kwargs['data_type']['ipv6_address']
        if 'data_type' in kwargs.keys():
            json_input['packet_dissection_objects'][0]['data_type'] = kwargs['data_type']
        logger.info(json_input)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp 

    def del_pdf_obj(self, name=None):
        url = self.url + '/name/' + name
        resp = self.fw.api_delete(url)
        return resp 

    def show_pdf_obj(self):
        resp = self.fw.api_get(self.url)
        return resp
        
    def add_pdf_group(self,msg=False, **kwargs):
        json_input = self.initial_pdf_group_json
        if 'name' not in kwargs.keys() or 'negative' not in kwargs.keys() or 'match_type' not in kwargs.keys():
            logger.error('Please specify name,negative,match_type when add pdf group.')
            return False
        json_input['packet_dissection_groups'][0]['name'] = kwargs['name']
        json_input['packet_dissection_groups'][0]['negative_matching'] = kwargs['negative']
        json_input['packet_dissection_groups'][0]['match_type'] = kwargs['match_type']
        if 'objects' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['packet_dissection_object'] =[]
            for object in kwargs['objects']:
                json_input['packet_dissection_groups'][0]['packet_dissection_object'].append({'name': object})
        if 'groups' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['packet_dissection_group'] =[]
            for group in kwargs['groups']:
                json_input['packet_dissection_groups'][0]['packet_dissection_group'].append({'name': group})
        resp = self.fw.api_post(self.url_group, msg, data=json_input)
        return resp 

    def edit_pdf_group(self, msg=False, **kwargs):
        json_input = self.initial_pdf_group_json
        if 'name' not in kwargs.keys():
            logger.error('Please specify name when edit pdf group.')
            return False
        url = self.url_group + '/name/' + kwargs['name']
        if 'name_new' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['name'] = kwargs['name_new']
        else:
            json_input['packet_dissection_groups'][0]['name'] = kwargs['name']
        if 'negative' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['negative_matching'] = kwargs['negative']
        if 'match_type' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['match_type'] = kwargs['match_type']
        if 'objects' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['packet_dissection_object'] =[]
            for object in kwargs['objects']:
                json_input['packet_dissection_groups'][0]['packet_dissection_object'].append({'name': object})
        if 'groups' in kwargs.keys():
            json_input['packet_dissection_groups'][0]['packet_dissection_group'] =[]
            for group in kwargs['groups']:
                json_input['packet_dissection_groups'][0]['packet_dissection_group'].append({'name': group})
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp 

    def del_pdf_group(self, name=None):
        url = self.url_group + '/name/' + name
        resp = self.fw.api_delete(url)
        return resp 

    def show_pdf_obj(self):
        resp = self.fw.api_get(self.url_group)
        return resp

class BlockPageApi:
    '''BlockPageApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/block-pages'

    def get_block_page(self):
        out = self.fw.api_get(self.url)
        return out

    def add_block_page(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        block_page_resp = self.fw.api_post(self.url, msg, data=json_input)
        return block_page_resp
    
class ServicesApi:
    '''ServicesApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/service-objects'

    def get_services(self):
        out = self.fw.api_get(self.url)
        return out
    
    def get_services_by_name(self, name):
        edit_url = self.url + '/name/' + name
        out = self.fw.api_get(edit_url)
        return out
    
    def add_service_objects(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp
    
    def delete_service_by_name(self, name, msg=False):
        edit_url = self.url + '/name/' + name
        out = self.fw.api_delete(edit_url, msg)
        return out