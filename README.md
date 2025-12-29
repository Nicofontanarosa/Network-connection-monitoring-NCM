# Network connection monitoring NCM

### What is Network connection monitoring NCM ?

Netstat Connection Monitoring is a network monitoring tool that runs multiple netstat commands with different parameters to analyze active network connections in real time. It is useful for understanding network behavior, tracking open sockets, and gaining visibility into system-level network activity.

![Static Badge](https://img.shields.io/badge/python-%20%3E%203.12-green?style=flat&labelColor=red&color=greed)
![Static Badge](https://img.shields.io/badge/license-MIT-blue)
<a href="https://github.com/Nicofontanarosa"><img src="https://img.shields.io/badge/powered_by-Nicofontanarosa-blueviolet"></a>

## ⚡ Features

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

---

# 🛠 How It Works

The script periodically executes different `netstat` commands and:
1. Collects raw connection data
2. Compares current connections with previous ones
3. Identifies new or changed entries
4. Logs updates to dedicated text files
5. Updates network statistics, routing tables, and processes every cycle

The monitoring loop runs every **5 seconds**.

---

# 📁 Log Files Generated

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

---

# 📌 Requirements

To run the `Net_Conn_Monitor.pyw` script, you need to have **Python** installed on your system ( *Tested on Python version >= 3.12* )
The script uses the following standard libraries, which are included in the Python Standard Library

- ✅ No external dependencies are required
- Operating System: **Windows** ( required for `netstat` flags used )

---

# 📄 License

This project is distributed under the terms of the MIT License. A complete copy of the license is available in the [LICENSE](LICENSE) file within this repository. Any contribution made to this project will be licensed under the same MIT License

- Author: Nicolò Fontanarosa
- Email: nickcompanyofficial@gmail.com
- Year: 2025

---

# 🙌 DISCLAIMER

While I do my best to detect location anomalies, I cannot guarantee that this software is error-free or 100% accurate. Please ensure that you respect users' privacy and have proper authorization to monitor, capture, and inspect network traffic

![GitHub followers](https://img.shields.io/github/followers/Nicofontanarosa?style=social)
