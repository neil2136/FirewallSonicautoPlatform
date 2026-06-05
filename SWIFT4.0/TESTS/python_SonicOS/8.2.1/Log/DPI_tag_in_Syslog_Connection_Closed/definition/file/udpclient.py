from socket import *

# 客户端发送一个请求也需要端口，端口是随机分配的
# 创建一个UDP协议的套接字，然后发送一条数据到网络上的另外一个进程

# UDP客户端、创建套接字
client_socket = socket(AF_INET, SOCK_DGRAM)  # SOCK_DGRAM:UDP协议

# 2、定义一个接收消息的目标,8080是一个目标服务器的端口，127.0.0.1是目标服务器地>址
server_host_port = ('12.12.1.200', 8080)
# 3、准备即将发送的数据,encode表示按照一种编码格式把数据变成字节数组bytes
# 数据一定是字节数据才能发送
datas = 'udp traffic test'.encode('utf-8')

# 4、发送数据,标识一个进程是通过ip+端口+协议
client_socket.sendto(datas, server_host_port)

print("send 'udp traffic test'")

# 5、关闭套接字，其实就是释放了系统资源
client_socket.close()
