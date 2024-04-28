import socket
import argparse
import threading
from queue import Queue

#User interface header
print(r""" Welcome to NITO's Port Scanner Tool """)
print("\n****************************************************************")
print("\n*                                                              *")
print("\n*             Welcome To NITO's Port Scanner Tool              *")
print("\n*                                                              *")
print("\n****************************************************************")


# Define common ports to scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389]

def scan_port(target_host, port, timeout=1):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(timeout)
        # Attempt to connect to the target host and port
        result = sock.connect_ex((target_host, port))
        # Check if the connection was successful
        if result == 0:
            print(f"Port {port} is open")
            # Attempt to grab the banner
            banner = sock.recv(1024).decode().strip()
            if banner:
                print(f"Banner for port {port}: {banner}")
        else:
            print(f"Port {port} is closed")
        # Close the socket
        sock.close()
    except KeyboardInterrupt:
        print("Scan stopped by user.")
        exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        exit()
    except socket.error:
        print("Couldn't connect to server.")
        exit()

def port_scan_worker(target_host, port_queue, timeout):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target_host, port, timeout)
        port_queue.task_done()

def scan_common_ports(target_host, timeout):
    print("Scanning common ports...")
    port_queue = Queue()
    # Enqueue common ports
    for port in COMMON_PORTS:
        port_queue.put(port)
    # Create and start threads
    for _ in range(10):  # You can adjust the number of threads here
        thread = threading.Thread(target=port_scan_worker, args=(target_host, port_queue, timeout))
        thread.start()
    # Wait for all threads to finish
    port_queue.join()

def main():
    parser = argparse.ArgumentParser(description="Network port scanner")
    parser.add_argument("host", help="Target host IP address")
    parser.add_argument("-r", "--range", help="Port range to scan (e.g., '1-1000')")
    parser.add_argument("-t", "--timeout", type=float, default=1, help="Connection timeout in seconds (default: 1)")
    parser.add_argument("-o", "--output", help="Output file to save scan results")
    args = parser.parse_args()

    target_host = args.host
    timeout = args.timeout

    if args.range:
        start_port, end_port = map(int, args.range.split('-'))
        for port in range(start_port, end_port + 1):
            scan_port(target_host, port, timeout)
    else:
        scan_common_ports(target_host, timeout)

    if args.output:
        with open(args.output, "w") as f:
            f.write("Scan results:\n")
            # Redirecting stdout to the file
            import sys
            sys.stdout = f
            main()
            # Reset stdout
            sys.stdout = sys.__stdout__
        print(f"Scan results saved to {args.output}")

if __name__ == "__main__":
    main()
