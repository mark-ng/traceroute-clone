# Build a traceroute clone

This is a simple traceroute clone used for study purposes. It uses Python and the raw socket module to send ICMP packets to a specified IP address with increasing TTL values. It then parses the ICMP response from routers to determine the path taken by the packets from the source to the destination.

## Implementation detail

- Create a raw socket to send ICMP packets
- Sends a series of 'Echo (ping) request' using the socket to a specified IP address with increasing TTL values
- Parse the ICMP response from routers
    - if it is 'Time-to-live exceeded', mean it is not the destination router
    - if it is 'Echo (ping) reply', mean it is the destination router, , traceroute is stopped
- if routers do not response before timeout, response will be skipped
- Measure the RTT of each request from three samples

## Usage

```bash
sudo python3 traceroute.py <destination>
```