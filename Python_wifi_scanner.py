#!/usr/bin/env python3
import scapy.all as scapy
import re

def print_header():
    print("*************************************************")
    print("*          Welcome to ARP Scanner Tool           *")
    print("*************************************************")

def get_ip_range():
    while True:
        ip_add_range_entered = input("\nPlease enter the IP address and subnet mask (ex: 192.168.1.0/24): ")
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$", ip_add_range_entered):
            return ip_add_range_entered
        else:
            print("Invalid IP address format. Please try again.")

def scan(ip_range):
    print("\nScanning...")
    arp_result = scapy.arping(ip_range)
    print("\nScan Results:")
    print(arp_result.summary())
    save_results(arp_result)

def save_results(scan_result):
    filename = input("\nEnter filename to save the results (default: scan_results.txt): ") or "scan_results.txt"
    with open(filename, "w") as file:
        file.write(str(scan_result))

def main():
    print_header()
    ip_range = get_ip_range()
    scan(ip_range)

if __name__ == "__main__":
    main()
