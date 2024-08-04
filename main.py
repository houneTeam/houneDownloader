import requests
from tqdm import tqdm
import os
import time
import logging
import socket
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("download.log"),
            logging.StreamHandler()
        ]
    )

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Check internet connection by trying to reach a reliable public DNS server.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def monitor_connection():
    """
    Continuously monitor internet connection and print status.
    """
    connection_status = is_connected()
    while True:
        current_status = is_connected()
        if current_status != connection_status:
            if current_status:
                logging.info(Fore.GREEN + "Internet connection is active.")
            else:
                logging.warning(Fore.RED + "Internet connection lost.")
            connection_status = current_status
        time.sleep(1)

def download_file(url, destination, chunk_size=1024):
    setup_logging()
    logging.info("Starting download process...")

    # Start a separate thread to monitor the connection
    import threading
    threading.Thread(target=monitor_connection, daemon=True).start()

    try:
        while True:
            # Wait for a valid internet connection
            while not is_connected():
                time.sleep(5)

            try:
                # Check if part of the file has already been downloaded
                if os.path.exists(destination):
                    # Get the size of the already downloaded part
                    current_size = os.path.getsize(destination)
                    resume_header = {'Range': f'bytes={current_size}-'}
                else:
                    current_size = 0
                    resume_header = {}

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
                }

                # Open the session
                with requests.get(url, headers={**headers, **resume_header}, stream=True) as r:
                    # Check if the server supports range requests
                    if r.status_code == 206 or r.status_code == 200:
                        total_size = int(r.headers.get('content-length', 0)) + current_size
                        with open(destination, 'ab') as f:
                            with tqdm(total=total_size, initial=current_size, unit='B', unit_scale=True, desc=destination) as pbar:
                                for chunk in r.iter_content(chunk_size=chunk_size):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)
                                        pbar.update(len(chunk))
                        logging.info(Fore.GREEN + "Download completed successfully!")
                        break
                    else:
                        logging.warning(Fore.RED + f"Server does not support range requests. Status code: {r.status_code}")
                        break
            except requests.ConnectionError:
                logging.warning(Fore.RED + "Connection error occurred. Retrying...")
                time.sleep(5)  # Pause before retrying
    except KeyboardInterrupt:
        logging.info(Fore.YELLOW + "\nDownload interrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        logging.error(Fore.RED + f"An unexpected error occurred: {e}")

url = "https://us.download.nvidia.com/RTX/ChatWithRTX_installer_3_5.zip"
destination = "ChatWithRTX_installer_3_5.zip"
download_file(url, destination)
