import sys
import subprocess

def block_ip(ip_address):
    print(f"Attempting to block IP: {ip_address}")
    try:
        command = ["ufw", "deny", "from", ip_address]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"SUCCESS: Firewall rule added to deny traffic from {ip_address}.")
        print(f"   Details: {result.stdout.strip()}")
    except FileNotFoundError:
        print("ERROR: 'ufw' command not found. Is the firewall installed and enabled?")
    except subprocess.CalledProcessError as e:
        print(f"ERROR executing firewall command for {ip_address}.")
        print(f"   Stderr: {e.stderr.strip()}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip_to_block = sys.argv[1]
        block_ip(ip_to_block)
    else:
        print("ERROR: Please provide an IP address to block.")
        print("   Usage: python3 block_ip.py <ip_address>")
