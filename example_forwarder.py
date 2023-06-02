from ipaddress import IPv4Address
import ipinip_lib


def main():
    ip = "127.0.0.14"
    port = 9890

    print(f"Forwarder listening at {ip}")

    while True:
        # Receive the message
        src_ip, dst_ip, payload_len = ipinip_lib.forward_fwd_packet(ip, port)

        # Deserialize the message and print it
        print(f"Forwarded package of size {payload_len} from {src_ip} to {dst_ip}:")


if __name__ == "__main__":
    main()
