import socket
import struct
from ipaddress import IPv4Address


def encapsulate_packet(src_ip, dst_ip, payload):
    # src_ip, dst_ip - ipv4 addresses from ipaddress library

    # Create the outer IP header
    header_format = '!BBHHHBBH4s4s'
    header_format_size = struct.calcsize(header_format)
    ip_header = struct.pack(header_format, 69, 0, len(payload) + header_format_size, 0, 0, 64, 4, 0, src_ip.packed,
                            dst_ip.packed)

    # Combine the outer IP header and the payload IP packet
    return ip_header + payload


def decapsulate_packet(packet):
    # Extract the payload IP packet from the IP-in-IP packet
    ip_header_length = (packet[0] & 0x0F) * 4
    return packet[ip_header_length:]


def send_packet(src_ip, dst_ip, payload, port):
    # Create an IP-in-IP packet
    packet = encapsulate_packet(src_ip, dst_ip, payload)

    # Send the packet
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as sender:  # todo debug
        # sender.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        sender.sendto(packet, (str(dst_ip), port))


def receive_packet(receiver_ip, receiver_port):
    # Receive the packet
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, 4) as receiver:
        receiver.bind((receiver_ip, receiver_port))
        packet, _ = receiver.recvfrom(65535)

    # Decapsulate the IP-in-IP packet
    payload = decapsulate_packet(packet)
    return payload
