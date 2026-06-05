import socket
import struct

from optparse import OptionParser


def send_dns_req(
    server, domain, port, id=0x1234, query_type=1, query_class=1, via="udp"
):
    try:
        # DNS query
        query = struct.pack("!H", id)
        query += struct.pack("!H", 0x0100)
        query += struct.pack("!H", 1)
        query += struct.pack("!H", 0)
        query += struct.pack("!H", 0)
        query += struct.pack("!H", 0)
        encode_domain = _encode_domain(domain)
        query += encode_domain
        query += struct.pack("!H", query_type)
        query += struct.pack("!H", query_class)

        # Send query via UDP / TCP
        resp = _sand_data("query", query, server, port, via)
        print("Send DNS query done.")
        return resp
    except Exception as e:
        print(f"Error when sending DNS query via {via} = {e}")
        return False


def send_dns_resp(
    host,
    domain,
    port,
    id=0x4321,
    query_type=1,
    query_class=1,
    ttl=300,
    length=4,
    ans_ip="1.2.4.8",
    via="udp",
):
    try:
        # Header
        header = struct.pack("!H", id)
        header += struct.pack("!H", 0x8780)
        header += struct.pack("!H", 1)
        header += struct.pack("!H", 1)
        header += struct.pack("!H", 0)
        header += struct.pack("!H", 0)

        # Question
        encode_domain = _encode_domain(domain)
        question = encode_domain
        question += struct.pack("!H", query_type)
        question += struct.pack("!H", query_class)

        # Answer
        answer = encode_domain
        answer += struct.pack("!H", query_type)
        answer += struct.pack("!H", query_class)
        answer += struct.pack("!I", ttl)
        answer += struct.pack("!H", length)
        answer += socket.inet_aton(ans_ip)

        # Response
        resp = header + question + answer
        # Send query response via UDP / TCP
        res = _sand_data("answer", resp, host, port, via)
        print("Send DNS query response done.")
        return res
    except Exception as e:
        print(f"Error when sending DNS query response via {via} = {e}")
        return False


def _encode_domain(domain):
    encode = b""
    for part in domain.split("."):
        encode += struct.pack("!B", len(part)) + part.encode()
    return encode + b"\x00"


def _sand_data(opt, data, host, port, via):
    if via == "udp":
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            if opt == "answer":
                sock.bind(("0.0.0.0", 53))
            sock.sendto(data, (host, int(port)))
            resp, _ = sock.recvfrom(512)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if opt == "answer":
                sock.bind(("0.0.0.0", 53))
            sock.connect((host, int(port)))
            sock.sendall(struct.pack("!H", len(data)) + data)
            resp = sock.recv(4096)
    return resp


def send_multi_query():
    # Operation = query | answer
    # Example:
    # python3 ./dnstest.py -o query -i 12.12.1.169 -p 53 -d testdomain.com -t udp -l 3

    parser = OptionParser()
    parser.add_option("-o", "--opt", dest="operation", help="Operation")
    parser.add_option("-i", "--host", dest="host", help="Host IP")
    parser.add_option("-p", "--port", dest="port", help="Port")
    parser.add_option("-d", "--domain", dest="domain", help="Domain Name")
    parser.add_option("-t", "--type", dest="via", help="Send Type")
    parser.add_option("-l", "--loop", dest="loop", help="Test Loop")
    parser.set_defaults(via="udp", loop=3, port=53)
    (options, _) = parser.parse_args()
    opt = options.operation
    host = options.host
    port = options.port
    domain = options.domain
    via = options.via
    loop = options.loop
    print(f"Will send DNS {opt} for {domain} to {host} via {via} for {loop} times")
    res = []
    for _ in range(int(loop)):
        if opt == "query":
            send_resp = send_dns_req(host, domain, port, via=via)
        else:
            send_resp = send_dns_resp(host, domain, port, via=via)
        res.append(send_resp)
    print(f"Send DNS {opt} results = {res}")
    return all(res)


if __name__ == "__main__":
    send_multi_query()
