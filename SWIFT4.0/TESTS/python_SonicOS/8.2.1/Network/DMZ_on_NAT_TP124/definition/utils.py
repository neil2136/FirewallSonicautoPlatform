def icmp_packet_check(resp, translated_src_ip, dst_ip, out_if):
    packets = resp.split('Packet number: ')
    icmptype = 'ICMP Type = 8' #request type
    translated_srcip = f'Src=[{translated_src_ip}]'
    dstip = f'Dst=[{dst_ip}]'
    packetinfo = f"out:{out_if}*, Forwarded"
    check_list = [icmptype, translated_srcip, dstip, packetinfo]
    for packet in packets:
        if all(item in packet for item in check_list):
            return True, packet
    return False, None