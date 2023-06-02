from ipaddress import IPv4Address
import ipinip_lib


def main():
    ip = "127.0.0.13"
    port = 9890
    print(f"Receiver listening at {ip}")

    while True:
        # Receive the message
        src_ip, dst_ip, message_payload = ipinip_lib.receive_direct_packet(ip, port)
        # ipinip_lib.listen_to_packets(ip, port)
        # Deserialize the message and print it
        message = message_payload.decode('utf-8')
        print(f"Received message from {src_ip}: {message}")


if __name__ == "__main__":
    main()
