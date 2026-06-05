def icmp_reply_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    result_packet = []
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    packettype = f"ICMP Type = 0(ECHO_REPLY)"
    for packet in packets:
        if srcip and dstip and packettype in packet:
            result_packet.append(packet)
    return result_packet


def icmp_drop_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    result_packet = []
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    packettype = f"ICMP Type = 8(ECHO_REQUEST)"
    drop = f"DROPPED"
    for packet in packets:
        if srcip and dstip and packettype and drop in packet:
            result_packet.append(packet)
    return result_packet
