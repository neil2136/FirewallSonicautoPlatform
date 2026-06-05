import argparse
import socket
import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from tools.trafficGen import  MyHttpClinet

parser = argparse.ArgumentParser(description='Process some parameter.')
parser.add_argument('--action',  type=int)
parser.add_argument('--addr', type=str)

args = parser.parse_args()
http_url = f'http://{args.addr}'
http_send = MyHttpClinet(http_url)
output = http_send.Http_get()
print(f'check {args.addr} http result: {output}')
if args.action == 2:
    print('action is allow , Connection established and Server side verification  should pass')
    if output:
        rc = True
        print("verify http sucess")
    else:
        rc = False
        print("verify http failed")
elif args.action == 0:
    print('action is deny,ping should failed')
    if output:
        rc = False
        print("verify http sucess")
    else:
        rc = True
        print("verify http failed")

# serveraddr = args.addr
# serverport = args.port
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
#     client_socket.connect((serveraddr, serverport))
#     if int(serverport) == 1720:
#         data="0300001c0802403c621c007e000e0528100004c00180050103280001"
#     else:
#         data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     client_socket.send(data.encode(encoding='utf_8',errors='strict'))
#     if int(serverport) != 1720:
#         msg = client_socket.recv(128).decode()
#         if msg == 'ZYXWVUTSRQPONMLKJIHGFEDCBA':
#             rc = True
#             logger.info("Received expected response data from the server")
#             print("Received expected response data from the server")
#             logger.info("Data transfer on TCP Session is verified")
#         elif msg == "":
#             rc = False
#             logger.info("No Response from the server")
#         else:
#             rc = False
#             logger.info("Received response data inconsistent with expected data from the server")
#     else:
#         logger.info("Received expected response data from the server")
#         print("Send expected response data to the server")

# client_socket.close()