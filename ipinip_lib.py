import socket
import struct
import time
from ipaddress import IPv4Address

def write_log(message):
    f = open("ipiniplog.txt", "a")
    f.write(str(time.time()) + "\t\t" + message + "\n")
    f.close()


def encapsulate_packet(src_ip, dst_ip, payload):

    # src_ip, dst_ip - ipv4 addresses from ipaddsress library

    # Create the outer IP header
    header_format = '!BBHHHBBH4s4s'
    header_format_size = struct.calcsize(header_format)
    ip_header = struct.pack(header_format, 69, 0, len(payload) + header_format_size, 0, 0, 64, 4, 0, src_ip.packed,
                            dst_ip.packed)
    write_log("Funkcja encapsulate_packet, ip header: " + str(ip_header) + ", payload: " + str(payload))
    # Combine the outer IP header and the payload IP packet
    return ip_header + payload


def decapsulate_packet(packet):
    # Extract the payload IP packet from the IP-in-IP packet
    ip_header_length = (packet[0] & 0x0F) * 4
    ip_header = struct.unpack('!BBHHHBBH4s4s', packet[:20])
    src_ip = socket.inet_ntoa(ip_header[8])
    dst_ip = socket.inet_ntoa(ip_header[9])
    write_log("Funkcja decapsulate_packet, ip header: " + str(ip_header))
    return src_ip, dst_ip, packet[ip_header_length:]


def send_fwd_packet(src_ip, fwd_ip, dst_ip, payload, port):
    # Create an IP packet
    layer_one_packet = encapsulate_packet(src_ip, dst_ip, payload)
    send_direct_packet(src_ip, fwd_ip, layer_one_packet, port)
    write_log("Funkcja send_fwd_packet stworzyła pakiet, Adresy IP: Źródło: " + str(src_ip) + " forwarder_ip: " + str(fwd_ip) + " Cel: " + str(dst_ip) + " Port: " + str(port) + " Payload: " + str(payload) )


def _ip_send(packet, dst_ip, port):
    # Send the packet
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as sender:
        sender.sendto(packet, (str(dst_ip), port))


def send_direct_packet(src_ip, dst_ip, payload, port):
    # Create IP packet
    packet = encapsulate_packet(src_ip, dst_ip, payload)
    _ip_send(packet, dst_ip, port)
    write_log("Funkcja send_direct_packet stworzyła pakiet, Adresy IP: Źródło: " + str(src_ip) + " Cel: " + str(dst_ip) + " Port: " + str(port) + " Payload: " + str(payload) )


def forward_fwd_packet(forwarder_ip, port):
    _src_ip, _fwd_ip, layer_two_packet = receive_direct_packet(forwarder_ip, port)
    src_ip, dst_ip, payload = decapsulate_packet(layer_two_packet)
    _ip_send(layer_two_packet, dst_ip, port)
    write_log("Funkcja forward_fwd_packet odebrała i przesłała wiadomość, Adres IP: " + str(forwarder_ip) + " Port: " + str(port))
    return src_ip, dst_ip, len(payload)


def receive_direct_packet(receiver_ip, port):
    # Receive the packet
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, 4) as receiver:
        receiver.bind((receiver_ip, port))
        packet, _ = receiver.recvfrom(65535)

    # Decapsulate the IP-in-IP packet
    src_ip, dst_ip, payload = decapsulate_packet(packet)
    write_log("Funkcja receive_direct_packet odebrała wiadomość, Adres IP: " + str(receiver_ip) + " Port: " + str(port))
    return src_ip, dst_ip, payload