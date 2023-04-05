from ipaddress import IPv4Address
import ipinip_lib


def main():
    src_ip = IPv4Address('10.1.1.100')  # sender IP address
    dst_ip = IPv4Address('10.1.1.200')  # receiver IP address
    port = 12345
    message = "sample text"

    # Serialize the message to send it as an IP packet
    message_payload = message.encode('utf-8')

    # Send the message
    ipinip_lib.send_packet(src_ip, dst_ip, message_payload, port)


if __name__ == "__main__":
    main()
