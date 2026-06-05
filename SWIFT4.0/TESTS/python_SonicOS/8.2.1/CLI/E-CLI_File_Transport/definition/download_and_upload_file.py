from ftplib import FTP
from definition.init_param import *

def ftp_upload(hostname, username, password, local_file_name, remote_file_name):
    local_file_path = f"/tmp/{local_file_name}"
    remote_file_path = f"/root/Downloads/cert/{remote_file_name}"
    try:
        # Connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        # Upload file
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f"STOR {remote_file_path}", file)

        ftp.quit()
        print("File upload successful!")
        return(True, "File upload successful!")
    except Exception as e:
        print("File upload failed:", e)
        return(False, f"File upload failed:{e}")

def ftp_download(hostname, username, password, remote_file_name, local_file_name):
    local_file_path = f"/tmp/ftp_log/{local_file_name}"
    remote_file_path = f"/tmp/ftp_log/{remote_file_name}"
    try:
        # Connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        # Download file
        with open(local_file_path, 'wb') as file:
            ftp.retrbinary(f"RETR {remote_file_path}", file.write)

        ftp.quit()
        print("File download successful!")
        return(True, "File download successful!")
    except Exception as e:
        print("File download failed:", e)
        return (False, f"File download failed:{e}")

def ftp_download_with_speed(hostname, username, password, remote_file_name, local_file_name):
    local_file_path = f"/tmp/{local_file_name}"
    remote_file_path = f"/root/Downloads/cert/{remote_file_name}"
    try:
        # Connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        # Get the size of the remote file
        remote_file_size = ftp.size(remote_file_path)

        # Download file
        start_time = time.time()
        with open(local_file_path, 'wb') as file:
            def download_callback(data):
                file.write(data)

            ftp.retrbinary(f"RETR {remote_file_path}", download_callback)

        download_time = time.time() - start_time
        download_speed = remote_file_size / download_time / 1024  # KB/s

        ftp.quit()
        print(f"File download successful! Download Speed: {download_speed:.2f} KB/s")
        return (True, f"File download successful! Download Speed: {download_speed:.2f} KB/s", download_speed)
    except Exception as e:
        print("File download failed:", e)
        return (False, f"File download failed: {e}")

def send_site_command(hostname, username, password, site_command):
    try:
        # Connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        # Send SITE command
        response = ftp.sendcmd(site_command)
        print("Response from SITE command:", response)

        ftp.quit()
        return (True,response)
    except Exception as e:
        print("Error:", e)
        return(False,e)



# Example usage:
# hostname = "192.168.13.200"
# username = "root"
# password = "password"
# local_file_name = "virus.doc"
# remote_file_name = "virus.doc"

# Upload file
# ftp_upload(hostname, username, password, local_file_path, remote_file_path)

# Download file
# ftp_download(hostname, username, password, remote_file_name, local_file_name)
