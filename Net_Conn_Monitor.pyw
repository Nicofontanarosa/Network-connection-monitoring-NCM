
import subprocess
import time
import logging
from datetime import datetime

# Triple quotes """ are used to represent multi-line strings or docstrings
# The first type is for strings declared on multiple lines without concatenation
# Example:
# text = """example of 
#     multi-line string"""

# Docstrings are used to document functions, classes, or modules in Python
# They appear as the first element within a function or class and describe its purpose or functionality

# You can access a function's docstring using its __doc__ attribute:
# print(get_active_connections.__doc__)

#* ----------------------------------------------------------------------
#? Functions relating to the initialization of log files

def log_initialization(previous_connections_diz, protocol_to_file):
    """-------- Fetch all active network connections using netstat --------"""
    try:

        # Initialize raw data storage
        raw_data_diz = {}
        # Fetch raw data for all protocols
        raw_data_diz['ALL'] = get_active_connections_raw()
        raw_data_diz['TCP'] = log_protocol_connections_raw('TCP')
        raw_data_diz['UDP'] = log_protocol_connections_raw('UDP')
        raw_data_diz['TCPv6'] = log_protocol_connections_raw('TCPv6')
        raw_data_diz['UDPv6'] = log_protocol_connections_raw('UDPv6')
        raw_data_diz['NetworkDirect'] = log_NetworkDirect_raw()

        # Write data to the respective log files
        for protocol, connections in raw_data_diz.items():
            log_file = protocol_to_file.get(protocol)

            if log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                with open(log_file, 'a') as f:
                    # Add a header with the timestamp
                    f.write(f"\n\n------------------- [{timestamp}] -------------------\n\n")
                    # Write raw data to the log file
                    f.write(f"{connections}\n")

        # Save the raw data in previous_connections_diz
        for protocol, connections in raw_data_diz.items():
            previous_connections_diz[protocol] = set(connections.splitlines())
            
    except Exception as e:
        logging.error(f"Error fetching all netstat connections: {e}")

#* ----------------------------------------------------------------------
#? Functions relating to netstat protocol

def get_active_connections_raw():
    """-------- Fetch the active network connections using netstat in row data --------"""
    try:

        # Run netstat and decode the output
        result = subprocess.run(['netstat', '-bonq'], capture_output=True, text=True, shell=True)
        # subprocess.run() executes a system command enclosed in []
        # capture_output captures the output written to stdout and the error written to stderr
        # text converts the byte output into a string
        # shell allows the system command to be executed within the shell
        return result.stdout
        # extracts the result

    except Exception as e:
        # f"write something {external_message} write something" is a way to include external variables within a string
        logging.error(f"Error fetching connections: {e}")


def log_connections(log_file, new_connections):
    """-------- Log new or changed connection data to the specified file --------"""
    # actual time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # open the file in path: log_file in append mode
    with open(log_file, 'a') as f:
        for connection in new_connections:
            # write time and new connection
            f.write(f"------------------- [{timestamp}] -------------------")
            f.write(f"\n\n{connection}\n\n")


def log_protocol_connections_raw(proto):
    """-------- Log network connections filtered by protocol in row data --------"""
    try:
        # Fetch netstat -p proto output ( connections for specific protocol )
        result = subprocess.run(['netstat', '-bonqp', proto], capture_output=True, text=True, shell=True)
        return result.stdout

    except Exception as e:
        logging.error(f"Error fetching protocol connections for {proto}: {e}")


def log_protocol_connections(proto, log_file, previous_connections):
    """-------- Log network connections filtered by protocol to the specified file --------"""
    try:
        # Fetch netstat -p proto raw output ( connections for specific protocol )
        current_connections = set(log_protocol_connections_raw(proto).splitlines())

        # Determine new or changed connections ( without time )
        new_connections = current_connections - previous_connections

        if new_connections:        
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a') as f:
                for connection in new_connections:
                    f.write(f"------------------- [{timestamp}] -------------------")
                    f.write(f"\n\n{connection}\n\n")
            # Update previous_connections with the current ones
            previous_connections.update(new_connections)

    except Exception as e:
        logging.error(f"Error fetching protocol connections for {proto}: {e}")


def log_NetworkDirect_raw():
    """-------- Log NetworkDirect connections in row data --------"""
    try:
        # Fetch netstat -xnq NetworkDirect quindi queste non sono connessioni di rete standard, ma piuttosto connessioni ad alte prestazioni
        result = subprocess.run(['netstat', '-xnq'], capture_output=True, text=True, shell=True)
        return result.stdout

    except Exception as e:
        logging.error(f"Error fetching connections: {e}")


def log_NetworkDirect(NetworkDirect_file, previous_connections):
    """-------- Log NetworkDirect connections --------"""
    try:
        current_connections = set(log_NetworkDirect_raw().splitlines())

        # Determine new or changed connections ( without time )
        new_connections = current_connections - previous_connections
        
        if new_connections:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(NetworkDirect_file, 'a') as f:
                for connection in new_connections:
                    f.write(f"------------------- [{timestamp}] -------------------")
                    f.write(f"\n\n{connection}\n\n")
            # Update previous_connections with the current ones
            previous_connections.update(new_connections)

    except Exception as e:
        logging.error(f"Error fetching connections: {e}")

#* ----------------------------------------------------------------------

def log_stats(stats_file):
    """-------- Log network statistics to the specified file by overwriting it --------"""
    try:
        # Fetch netstat -se output (network statistics)
        result = subprocess.run(['netstat', '-se'], capture_output=True, text=True, shell=True)
        with open(stats_file, 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")


def log_routing(routing_file):
    """-------- Log routing table to the specified file by overwriting it --------"""
    try:
        result = subprocess.run(['netstat', '-r'], capture_output=True, text=True, shell=True)
        with open(routing_file, 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")


def log_processes(processes_file):
    """-------- Log processes to the specified file by overwriting it --------"""
    try:
        result = subprocess.run(['netstat', '-c'], capture_output=True, text=True, shell=True)
        with open(processes_file, 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")

#* ----------------------------------------------------------------------
#? Run the application

def monitor_connections():
    """-------- Continuously monitor and log active network connections --------"""
    #? Data
    # Files in append mode
    log_file = "connection_log.txt"
    tcp_log_file = "tcp_connections.txt"
    udp_log_file = "udp_connections.txt"
    tcpv6_log_file = "tcpv6_connections.txt"
    udpv6_log_file = "udpv6_connections.txt"
    NetworkDirect_file = "NetworkDirect_connections.txt"
    # Files in write mode
    stats_file = "network_stats.txt"
    routing_file = "routing_table.txt"
    processes_file = "processes_log.txt"
    # Define a mapping between protocols and past connections
    previous_connections_diz = {
        'ALL': set(),
        'TCP': set(),
        'UDP': set(),
        'TCPv6': set(),
        'UDPv6': set(),
        'NetworkDirect': set()
    }
    # Define a mapping between log files and protocols
    protocol_to_file = {
        'ALL': log_file,
        'TCP': tcp_log_file,
        'UDP': udp_log_file,
        'TCPv6': tcpv6_log_file,
        'UDPv6': udpv6_log_file,
        'NetworkDirect': NetworkDirect_file
    }
    #? Start program
    # Log initialization with raw data of netstat result
    log_initialization(previous_connections_diz, protocol_to_file)

    # Configures the logging library to print informational messages to the terminal
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # Specifies that "INFO" level messages or higher will be logged
    # Prints an initial message to the terminal
    logging.info("Starting network connection monitor...\n")

    while True:

        try:
            # Fetch current active connections ( raw output )
            raw_output = get_active_connections_raw()
            # Splits the lines to analyze the connections
            current_connections = set(raw_output.splitlines())

            # Determine changed connections ( without time )
            new_connections = current_connections - previous_connections_diz['ALL']

            if new_connections:

                previous_connections_diz['ALL'] = current_connections
                # Log changes to the terminal
                for conn in new_connections:
                    logging.info(f"New / changed connection: {conn}")

                # Write to log file
                log_connections(log_file, new_connections)

                # Log protocol-specific connections every 5 seconds ( if thers a general new / modified connection )
                log_protocol_connections('TCP', tcp_log_file, previous_connections_diz['TCP'])
                log_protocol_connections('UDP', udp_log_file, previous_connections_diz['UDP'])
                log_protocol_connections('TCPv6', tcpv6_log_file, previous_connections_diz['TCPv6'])
                log_protocol_connections('UDPv6', udpv6_log_file, previous_connections_diz['UDPv6'])
                log_NetworkDirect(NetworkDirect_file, previous_connections_diz['NetworkDirect'])

            # Log network stats, routing tables and processes every 5 seconds (overwrite the stats file)
            log_stats(stats_file)
            log_routing(routing_file)
            log_processes(processes_file)
                
            # Wait before the next check
            time.sleep(5)

        except KeyboardInterrupt:
            # Manual user interruptions
            logging.info("Monitoring stopped by user")
            break
        except Exception as e:
            # Interruptions during monitoring
            logging.error(f"Error during monitoring: {e}")

# When Python executes a file, it defines a special variable called __name__
# If the file is executed directly, for example, with "py file_name.py", the __name__ variable is set to "__main__"
# This ensures that the code inside this block is executed only if the file is run directly and not when it is imported
if __name__ == "__main__":
    monitor_connections()

# Python has various logging levels that represent the importance or severity of messages
# This is useful for categorizing the messages logged during program execution
# Main levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Example: logging.basicConfig( level=logging.INFO )
# logging.debug( "Debug message" )         # Will not be displayed ( level too low )
# logging.info( "Useful information" )    # Will be displayed
# logging.warning( "Something is wrong" ) # Will be displayed
# logging.error( "Critical error" )       # Will be displayed
# logging.critical( "System crash" )      # Will be displayed
# DEBUG-level messages will not be shown, whereas WARNING, ERROR, and CRITICAL messages will
# The logging library allows you to do much more compared to a classic print statement
