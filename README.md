# Resumable File Downloader with Connection Monitoring

This Python script provides a robust solution for downloading large files over unstable internet connections. It continuously monitors the internet connection and can resume downloads automatically after a connection drop. The script also provides a progress bar and colored console output for easy tracking of download status.

## Description

This is a powerful downloader script designed to handle unstable internet connections. Whether you're dealing with intermittent connectivity or frequent drops, this downloader will seamlessly resume and complete your downloads. Perfect for large files and unreliable networks, it ensures you get what you need, no matter the connection challenges.

![Description](https://github.com/houneTeam/houneDownloader/blob/main/image.png?raw=true)

## Features

- **Resumable Downloads:** Automatically resumes downloading if the connection is lost and restored.
- **Connection Monitoring:** Continuously checks the internet connection status and logs changes.
- **Colored Console Output:** Uses colors to indicate connection status and errors for better visibility.
- **Progress Bar:** Displays a progress bar for the download process.

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library
- `colorama` library

## Installation

1. Clone the repository:

   git clone https://github.com/houneTeam/houneDownloader.git
   cd houneDownloader

2. Install the required Python packages:

   pip install requests tqdm colorama

## Usage

1. Edit the script to set your desired download URL and destination file path:

   url = "https://us.download.nvidia.com/RTX/ChatWithRTX_installer_3_5.zip"
   destination = "ChatWithRTX_installer_3_5.zip"

2. Run the script:

   python main.py

## How It Works

- The script checks if the internet connection is active before starting or resuming the download.
- It uses the `Range` HTTP header to resume downloads from where they were interrupted.
- A separate thread continuously monitors the internet connection and logs changes in status to the console.
- The script can be interrupted safely with `Ctrl+C`, which will stop the download process gracefully.

## Customization

You can customize the script by modifying the following:

- **Chunk Size:** Change the `chunk_size` parameter in the `download_file` function to adjust the amount of data downloaded in each iteration.
- **Connection Check Interval:** Adjust the sleep interval in the `monitor_connection` function for more or less frequent checks.

## Troubleshooting

- **Connection Issues:** Ensure your internet connection is stable or increase the retry interval if you encounter frequent drops.
- **Permission Errors:** Run the script with appropriate permissions if you encounter file access issues.

## Acknowledgments

- [requests](https://github.com/psf/requests) - HTTP library for Python.
- [tqdm](https://github.com/tqdm/tqdm) - A fast, extensible progress bar for Python.
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text in Python.
