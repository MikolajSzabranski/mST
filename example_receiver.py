from ipaddress import IPv4Address
import ipinip_lib


def main():
    ip = "10.1.1.184"
    port = 12345

    # Receive the message
    message_payload = ipinip_lib.receive_packet(ip, port)
    #ipinip_lib.listen_to_packets(ip, port)
    # Deserialize the message and print it
    message = message_payload.decode('utf-8')
    print("Received message:", message)


if __name__ == "__main__":
    main()
