import sys
import socket

def traceroute(domain, max_ttl):
    ip = socket.gethostbyname(domain)
    print(f"traceroute to {domain} ({ip}), {max_ttl} hops max")

if __name__ == '__main__':
    assert len(sys.argv) == 2
    domain = sys.argv[1]

    # Config
    max_ttl = 64

    traceroute(domain, max_ttl)