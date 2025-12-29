# Network connection monitoring NCM

### What is Network connection monitoring NCM ?

Netstat Connection Monitoring is a network monitoring tool that runs multiple netstat commands with different parameters to analyze active network connections in real time. It is useful for understanding network behavior, tracking open sockets, and gaining visibility into system-level network activity.

![Static Badge](https://img.shields.io/badge/python-%20%3E%203.12-green?style=flat&labelColor=red&color=greed)
![Static Badge](https://img.shields.io/badge/license-MIT-blue)
<a href="https://github.com/Nicofontanarosa"><img src="https://img.shields.io/badge/powered_by-Nicofontanarosa-blueviolet"></a>

## Features

- Continuous monitoring of active network connections
- Detection of new or modified connections
- Protocol-specific logging:
  - TCP
  - UDP
  - TCPv6
  - UDPv6
  - NetworkDirect
- Logging of:
  - Active connections
  - Network statistics
  - Routing table
  - Network-related processes
- Timestamped logs for easier tracking
- Console output for real-time visibility

## How It Works

The script periodically executes different `netstat` commands and:
1. Collects raw connection data
2. Compares current connections with previous ones
3. Identifies new or changed entries
4. Logs updates to dedicated text files
5. Updates network statistics, routing tables, and processes every cycle

The monitoring loop runs every **5 seconds**.

## Log Files Generated

| File Name | Description |
|---------|-------------|
| `connection_log.txt` | All detected network connections |
| `tcp_connections.txt` | TCP connections |
| `udp_connections.txt` | UDP connections |
| `tcpv6_connections.txt` | TCPv6 connections |
| `udpv6_connections.txt` | UDPv6 connections |
| `NetworkDirect_connections.txt` | High-performance NetworkDirect connections |
| `network_stats.txt` | Network statistics (`netstat -se`) |
| `routing_table.txt` | Routing table (`netstat -r`) |
| `processes_log.txt` | Network-related processes |

## Requirements

- Python 3.x
- Operating System: **Windows** (required for `netstat` flags used)

### Python Standard Libraries Used
No external Python libraries are required.
The script uses only:
- `subprocess`
- `time`
- `logging`
- `datetime`

## Usage

Run the script directly:

```bash
python monitor.py

