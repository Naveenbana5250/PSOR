import yaml
import subprocess
import sys

def main():
    """
    The main function for the orchestration engine.
    """
    print("Engine starting...")

    # Load the playbook
    try:
        with open('playbook.yml', 'r') as file:
            playbook = yaml.safe_load(file)
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error loading playbook: {e}")
        return # Exit if playbook fails to load

    print(f"Successfully loaded playbook: '{playbook.get('name')}'")

    # Execute steps from the playbook
    for step in playbook.get('steps', []):
        action = step.get('action')
        parameters = step.get('parameters', {})
        print(f"\n▶️  Executing step: '{step.get('name')}'")

        if action == 'block_ip':
            ip = parameters.get('ip_address')
            if ip:
                # Construct the command to run the plugin script
                command = [sys.executable, "plugins/block_ip.py", ip]
                subprocess.run(command)
            else:
                print("❌ Error: 'ip_address' not specified in parameters for block_ip action.")
        else:
            print(f"⚠️  Warning: Action '{action}' is not supported.")

if __name__ == "__main__":
    main()
