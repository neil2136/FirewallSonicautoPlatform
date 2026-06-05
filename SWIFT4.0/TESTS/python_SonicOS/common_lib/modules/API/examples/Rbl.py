import os,sys
import json
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../'
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.Rbl import RblAPI

ip = '10.5.192.38'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
url='/rbl'


Rbl=RblAPI(fw)


def test_get_rbl_using_name():
    print("-------------------------------get---------------------------------")
    url='/rbl/services/domain/abcd.com'
    response=Rbl.get_rbl(url)
    print("-------------------------------Out Put:---------------\n",response)
def test_put_rbl():
    print("------------------------------put-----------------------------------")
    rbl={
    "rbl": {
       
        "service": [
            {
                "domain": "abcd.com",
                  "blocked_responses": {
                    "block_all": False
                }
               
            }
        ]
    }
}
    
    response=Rbl.edit_rbl (**rbl)

def DELETE_rbl_service():
    print("-----------------------------------Delete----------------------------------")
    rbl={
    "rbl": {
       
        "service": [
            {
                "domain": "abcd.com"
               
               
            }
        ]
    }
}
    url='/rbl/services/domain/abcd.com'
    response=Rbl.delete_rbl(url)
    print(response)

def test_post_rbl():
    print("------------------------------post-----------------------------------")
    rbl={
    "rbl": {
       
        "service": [
            {
                "domain": "abcd.com",
                  "blocked_responses": {
                    "block_all": True
                }
               
            }
        ]
    }
}

    
    response=Rbl.create_rbl (**rbl)


test_post_rbl()
test_get_rbl_using_name()
test_put_rbl()
DELETE_rbl_service()



