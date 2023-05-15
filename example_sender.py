from ipaddress import IPv4Address
import ipinip_lib


def main():
    src_ip = IPv4Address('10.1.1.186')  # sender IP address
    fwd_ip = IPv4Address('127.0.0.14')  # forwarder IP address
    dst_ip = IPv4Address('127.0.0.13')  # receiver IP address
    port = 12345

    print(f"IP-in-IP sender initialized at {src_ip}")
    print(f"Forwarding through {fwd_ip} to {dst_ip}")
    print("Waiting for user input...")
    while True:
        message = input()

        # Serialize the message to send it as an IP packet
        message_payload = message.encode('utf-8')

        # Send the message
        ipinip_lib.send_fwd_packet(src_ip, fwd_ip, dst_ip, message_payload, port)


if __name__ == "__main__":
    main()
