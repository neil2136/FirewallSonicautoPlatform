import json
import copy
  
from util.snwl_logging import logger
from util.assertion import *


class AntiSpamAPI():



    global anti_spam_url
    anti_spam_url= '/anti-spam/settings'
    def __init__(self,fw):
        self.fw = fw
        global anti_spam_url
        
        self.general_url= '/api/sonicos'
        self.default_remover=\
        {
           
        }

        self.tracker=[]
        self.initial_anti_spam_copy=False

        #initializing the initial dictionary
        self.initial_anti_spam_json= {
            'anti_spam': {
                'enable': False,
                'action': {
                    'likely_spam': 'store',
                    'definite_spam': 'delete',
                    'likely_phishing': 'tag',
                    'definite_phishing': 'store',
                    'likely_virus': 'store',
                    'definite_virus': 'delete'
                },
                'service_down': 'allow',
                'junk_box': {
                    'down': 'tag-deliver'
                },
                'probe': {
                    'interval': 5,
                    'timeout': 30 
                },
                'success_threshold': 1,
                'failure_threshold': 3,
                'mail_server': {
                    'public': '0.0.0.0',
                    'private': '0.0.0.0',
                    'port': 25
                },
                'destination_mail_address_as_junk_store': True,
                'system_detection': True
            }
        }

    #Scaning each keys,values and updates in initial json
    def auto_key_value_replacer(self,input_dictionary):#change the name input_dictionory
        if not self.initial_anti_spam_copy:
            self.initial_anti_spam_copy = copy.deepcopy(self.initial_anti_spam_json)
        if str(type(input_dictionary))== "<class 'list'>" :
            index_counter=0
            temp=self.initial_anti_spam_copy
            for i in self.tracker:
                    temp=temp[i]
                    if i==self.tracker[len(self.tracker)-1]:
                        if not len(temp) == len(input_dictionary):
                            for key in range(0,len(input_dictionary)):
                                if len(temp) < key+1:
                                    temp.append(input_dictionary[key])
                        break
            #t=0        
            for key in input_dictionary:
                #t=t+1
                index_counter=index_counter+1
                self.tracker.append(index_counter-1)
                self.auto_key_value_replacer(key)
            self.tracker.pop()
                
        elif str(type(input_dictionary))== "<class 'dict'>" :
            t=0
            for key in input_dictionary.keys():
                temp=self.initial_anti_spam_copy
                for i in self.tracker:
                    temp=temp[i]
                    if i==self.tracker[len(self.tracker)-1]:
                        if not key in temp.keys():
                            temp[key]=copy.deepcopy(input_dictionary[key])
                            break
                t=t+1
                self.tracker.append(str(key))
                self.auto_key_value_replacer(input_dictionary[key])
            if t == len(input_dictionary) and len(self.tracker) > 0 :
                self.tracker.pop()
                               
        elif str(type(input_dictionary))== "<class 'str'>" or str(type(input_dictionary))== "<class 'int'>" or str(type(input_dictionary))== "<class 'bool'>" :
            p='self.initial_anti_spam_copy'
            for elements in self.tracker:
                if str(type(elements)) ==  "<class 'str'>":
                    p=p+'["{}"]'.format(elements)
                else:
                    p=p+'[{}]'.format(elements)
            if p in self.default_remover.keys():
                exec(self.default_remover[p])
            if str(type(input_dictionary)) ==  "<class 'str'>":
                p=p+'="{}"'.format(input_dictionary)
            else:
                p=p+'={}'.format(input_dictionary)
            exec(p)
            self.tracker.pop()
    
    #Mehtod to build json to send 
    def build_json_anti_spam(self,**anti_spam):
        self.initial_anti_spam_copy={}
        self.auto_key_value_replacer(anti_spam)
        return self.initial_anti_spam_copy
     
    #Mthod to Delete the antispam configuration 
    print(anti_spam_url)
    def delete_antispam(self,url=anti_spam_url,msg=False,data=None):
        final_url=self.general_url+url
        logger('URL for Delete:- ',final_url)
        delete_resp = self.fw.api_delete(final_url,data=data)
        return delete_resp

    # Method to GET all the anti spam details.
    def get_antispam(self,url=anti_spam_url):
        final_url=self.general_url+url
        logger('URL for Get:- ',final_url)
        get_response = self.fw.api_get(final_url)
        return get_response

    # Method to modify the anti spam details.
    def edit_antispam (self,url=anti_spam_url,msg=False,**anti_spam):
        final_url=self.general_url+url
        if final_url == '/api/sonicos/anti-spam/settings':
            initial_anti_spam_json=self.build_json_anti_spam(**anti_spam)
        else:
            initial_anti_spam_json=anti_spam
        logger('URL for posting',final_url)
        post_response=self.fw.api_put(final_url,data=initial_anti_spam_json)
        return post_response


class RblAPI():

    global Rbl_url
    rbl_url = '/rbl'

    def __init__(self, fw):
        self.fw = fw
        self.general_url = '/api/sonicos'
        self.default_remover =\
            {

            }

        self.tracker = []
        self.initial_rbl_copy = False

        #initializing the initial dictionary
        self.initial_rbl_json = {
            "rbl": {
                "enable": False,
                "dns": {
                    "inherit": True
                },
                "service": [
                    {
                        "domain": "sbl-xbl.spamhaus.org",
                        "enable": True,
                        "blocked_responses": {
                            "block_all": True
                        }
                    },
                    {
                        "domain": "dnsbl.sorbs.net",
                        "enable": True,
                        "blocked_responses": {
                            "block_all": True
                        }
                    }
                ]
            }
        }

    #Scaning each keys,values and updates in initial json
    def auto_key_value_replacer(self, input_dictionary):
        #condition for creating a copy of initial json
        if not self.initial_rbl_copy:
            self.initial_rbl_copy = copy.deepcopy(
                self.initial_rbl_json)

        #condition for list keys
        if str(type(input_dictionary)) == "<class 'list'>":
            index_counter = 0
            temp = self.initial_rbl_copy
            for i in self.tracker:
                    temp = temp[i]
                    if i == self.tracker[len(self.tracker)-1]:
                        if not len(temp) == len(input_dictionary):
                            for key in range(0, len(input_dictionary)):
                                if len(temp) < key+1:
                                    temp.append(input_dictionary[key])
                        break
            #t=0
            
            #checking keys type inside the list
            for key in input_dictionary:
                #t=t+1
                index_counter = index_counter+1
                self.tracker.append(index_counter-1)
                self.auto_key_value_replacer(key)
            #reseting the tracker after successfully exicuting each elements inside list
            self.tracker.pop()

        #condition for dict keys
        elif str(type(input_dictionary)) == "<class 'dict'>":
            t = 0
            for key in input_dictionary.keys():
                temp = self.initial_rbl_copy
                for i in self.tracker:
                    temp = temp[i]
                    if i == self.tracker[len(self.tracker)-1]:
                        if not key in temp.keys():
                            temp[key] = copy.deepcopy(input_dictionary[key])
                            break
                t = t+1
                self.tracker.append(str(key))
                self.auto_key_value_replacer(input_dictionary[key])
            if t == len(input_dictionary) and len(self.tracker) > 0:
                self.tracker.pop()

        #condition for str,int,bool keys
        elif str(type(input_dictionary)) == "<class 'str'>" or str(type(input_dictionary)) == "<class 'int'>" or str(type(input_dictionary)) == "<class 'bool'>":
            p = 'self.initial_rbl_copy'
            for elements in self.tracker:
                if str(type(elements)) == "<class 'str'>":
                    p = p+'["{}"]'.format(elements)
                else:
                    p = p+'[{}]'.format(elements)
            if p in self.default_remover.keys():
                exec(self.default_remover[p])
            if str(type(input_dictionary)) == "<class 'str'>":
                p = p+'="{}"'.format(input_dictionary)
            else:
                p = p+'={}'.format(input_dictionary)
            exec(p)
            self.tracker.pop()


    #Mehtod to build json to send
    def build_json_rbl(self, **rbl):
        self.initial_rbl_copy = {}
        self.auto_key_value_replacer(rbl)
        return self.initial_rbl_copy

    #Mthod to Delete the rbl configuration
    def delete_rbl(self, url=rbl_url, msg=False, data=None):
        final_url = self.general_url+url
        logger('URL for Delete:- ', final_url)
        delete_resp = self.fw.api_delete(final_url, data=data)
        return delete_resp

    # Method to GET all the anti spam details.
    def get_rbl(self, url=rbl_url):
        final_url = self.general_url+url
        logger('URL for Get:- ', final_url)
        get_response = self.fw.api_get(final_url)
        return get_response

    # Method to modify the anti spam details.
    def create_rbl(self, url=rbl_url, msg=False, **rbl):
        final_url = self.general_url+url
        #if final_url == '/api/sonicos/anti-spam/settings':
        initial_rbl_json = self.build_json_rbl(**rbl)
        #else:
        #    initial_rbl_json = rbl
        logger('URL for posting', final_url)
        print(initial_rbl_json)
        post_response = self.fw.api_post(final_url, data=rbl)
        return post_response

    # Method to modify the anti spam details.
    def edit_rbl(self, url=rbl_url, msg=False, **rbl):
        final_url = self.general_url+url
        #if final_url == '/api/sonicos/anti-spam/settings':
        initial_rbl_json = self.build_json_rbl(**rbl)
        #else:
        #    initial_rbl_json = rbl
        logger('URL for posting', final_url)
        print(initial_rbl_json)
        post_response = self.fw.api_put(final_url, data=initial_rbl_json)
        return post_response
