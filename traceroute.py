import sys
import socket
import struct
import random

def parse_icmp(b):
    # Skip IP Header
    type, code = struct.unpack("!BB", b[20:22])
    return type, code

def cal_checksum(type, code, identifier, sequence_number, data):
    data_sum = sum(struct.unpack("!24H", data))
    return (struct.unpack("!H", struct.pack("!BB", type, code))[0] + 0 + identifier + \
    sequence_number + data_sum) ^ 0xFFFF
    
def traceroute(domain, max_ttl):
    ip = socket.gethostbyname(domain)
    print(f"traceroute to {domain} ({ip}), {max_ttl} hops max")

    ttl = 1
    is_over = False

    # Loop until the Type change from 'Time-to-live exceeded' to 'Echo (ping) reply'
    # TODO: Bug 3 samples from the same address
    while True:

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(2)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        # ICMP Header
        type = 8
        code = 0
        identifier = 0
        sequence_number = 0

        # Genereate 3 sample
        for i in range(3):
            # ICMP Data
            random_data = [int(random.uniform(1, 1000)) for i in range(12)]
            data = struct.pack("!12I", *random_data)

            # Calculate Checksum
            checksum = cal_checksum(type, code, identifier, sequence_number, data)

            # Construct ICMP Header
            b = struct.pack("!BBHHH", type, code, checksum, identifier, sequence_number)

            sock.sendto(b + data, (ip, 80))

            try:
                content, from_addr = sock.recvfrom(2000)
                return_type, return_code = parse_icmp(content)
                # Echo (ping) reply
                if return_type == 0 and return_code == 0 and i == 2:
                    print(f"{ttl} ({from_addr[0]})")
                    is_over = True
                    break
            except socket.timeout:
                if i == 2:
                    print("*", flush=True)
                else:
                    print("*", end = " ", flush=True)
                continue
            else:
                print(f"{ttl} ({from_addr[0]})")

        if is_over:
            break

        print()
        ttl += 1

    sock.close()

if __name__ == '__main__':
    assert len(sys.argv) == 2
    domain = sys.argv[1]

    # Config
    max_ttl = 64

    traceroute(domain, max_ttl)