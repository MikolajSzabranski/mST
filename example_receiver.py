from ipaddress import IPv4Address
import ipinip_lib


def main():
    port = 12345

    # Receive the message
    message_payload = ipinip_lib.receive_packet(port)

    # Deserialize the message and print it
    message = message_payload.decode('utf-8')
    print("Received message:", message)


if __name__ == "__main__":
    main()
