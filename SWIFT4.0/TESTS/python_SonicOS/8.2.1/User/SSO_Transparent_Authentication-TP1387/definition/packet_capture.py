import paramiko
import subprocess
import os
import time

def ssh_execute_command(host, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    ssh.close()

    if error:
        raise Exception(f"Error executing command: {error}")
    return output


def capture_udp_packets(interface_index, capture_duration, output_file):
    dumpcap_path = r"C:\Program Files\Wireshark\dumpcap.exe"

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [
        dumpcap_path,
        "-i", str(interface_index),
        "-f", "udp",
        "-a", f"duration:{capture_duration}",
        "-w", output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Packet capture complete. Saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while capturing packets: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def search_in_pcap(pcap_file, search_string):
    tshark_path = r"C:\Program Files\Wireshark\tshark.exe"
    command = [
        tshark_path,
        "-r", pcap_file,
        "-Y", f'frame contains "{search_string}"'
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        return search_string in output
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while searching packets: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    host = "remote_host_ip"
    port = 22
    username = "your_username"
    password = "your_password"

    ssh_command = "your_command_here"

    interface_index = 2
    capture_duration = 60  # Duration in seconds
    output_file = r"C:\path\to\output\udp_capture.pcap"

    try:
        output = ssh_execute_command(host, port, username, password, ssh_command)
        print(f"SSH command output: {output}")

        capture_udp_packets(interface_index, capture_duration, output_file)

        search_string = "agent is ready"
        if search_in_pcap(output_file, search_string):
            print(f"Assertion passed: '{search_string}' found in the pcap file.")
        else:
            print(f"Assertion failed: '{search_string}' not found in the pcap file.")

    except Exception as e:
        print(f"An error occurred: {e}")
