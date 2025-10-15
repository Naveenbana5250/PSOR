import yaml
import subprocess
import sys
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename='audit.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def load_policies():
    try:
        with open('policies.yml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}

def main():
    setup_logging()
    policies = load_policies()
    denied_ips = policies.get('safety_policies', {}).get('denied_ips', [])
    logging.info("Engine starting...")

    try:
        with open('playbook.yml', 'r') as file:
            playbook = yaml.safe_load(file)
    except (FileNotFoundError, yaml.YAMLError) as e:
        logging.error(f"Error loading playbook: {e}")
        print(f"Error loading playbook: {e}")
        return

    playbook_name = playbook.get('name', 'Unnamed Playbook')
    logging.info(f"Successfully loaded playbook: '{playbook_name}'")
    print(f"Successfully loaded playbook: '{playbook_name}'")

    for step in playbook.get('steps', []):
        step_name = step.get('name', 'Unnamed Step')
        action = step.get('action')
        parameters = step.get('parameters', {})
        logging.info(f"Executing step: '{step_name}'")
        print(f"\nExecuting step: '{step_name}'")

        if action == 'block_ip':
            ip = parameters.get('ip_address')
            if not ip:
                logging.error("'ip_address' not specified for block_ip action.")
                print("ERROR: 'ip_address' not specified for block_ip action.")
                continue

            if ip in denied_ips:
                logging.warning(f"SAFETY VIOLATION: Action 'block_ip' on '{ip}' denied by policy.")
                print(f"SAFETY VIOLATION: Action on '{ip}' denied by policy.")
                continue

            command = ["python3", "plugins/block_ip.py", ip]
            result = subprocess.run(command)
            if result.returncode == 0:
                logging.info(f"Step '{step_name}' completed successfully.")
            else:
                logging.error(f"Step '{step_name}' failed with return code {result.returncode}.")
        else:
            logging.warning(f"Action '{action}' is not supported.")
            print(f"WARNING: Action '{action}' is not supported.")

if __name__ == "__main__":
    main()
