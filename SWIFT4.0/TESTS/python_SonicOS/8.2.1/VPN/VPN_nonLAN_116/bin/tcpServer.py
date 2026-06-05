import argparse
import socket
import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from tools.trafficGen import  MyHttpClinet

parser = argparse.ArgumentParser(description='Process some parameter.')
parser.add_argument('--port',  type=int)
parser.add_argument('--addr', type=str)

args = parser.parse_args()

# localaddr = args.addr
# localport = args.port
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((localaddr, localport))
#     server_socket.listen(5)
#     conn, addr = server_socket.accept()
#     with conn:
#         print(f'Connection from: {addr}')
#         data = conn.recv(128).decode()
#         #TBD_SD_11/20/03 To Add Buffering Capabilities on the Server
#         ##H323 is a special case for this generic tcp server because of extra-stateful validation at firewall 
#         if int(localport) == 1720:
#             if data !="0300001c0802403c621c007e000e0528100004c00180050103280001":
#                 rc  = False
#                 print("Expected not gotten from client for H323\n")
#                 print(data)
#             else:
#                 rc = True
#                 print("Connection established and Server side verification passed\n")
#         else:
#             if data == "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                 conn.send(("ZYXWVUTSRQPONMLKJIHGFEDCBA").encode(encoding='utf_8',errors='strict'))
#                 rc = True
#                 print("Connection established and Server side verification passed\n")
#             else:
#                 rc = False
#                 print("Expected not gotten from client for client")
#                 print(data)
       
