import socket
import struct
import sys

if len(sys.argv) < 2:
    print('ERROR: Please check the parameters!')
    sys.exit()


def send_magic_packet(mac_address):
    # WOL 使用 UDP 协议的端口 9 发送魔术包
    dest_ip = '255.255.255.255'
    dest_port = 9

    # MAC 地址需要转换成二进制形式
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))

    # 构建魔术包
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # 发送魔术包
    sock.sendto(magic_packet, (dest_ip, dest_port))
    sock.close()

# 调用函数发送 WOL 包
if __name__ == '__main__':
    send_magic_packet('00:11:22:33:44:55')
