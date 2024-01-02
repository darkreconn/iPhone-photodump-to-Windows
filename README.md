<b>Media File Transfer/Backup Script</b>
<hr>
Overview:
- This Python script facilitates the seamless transfer of photos & videos from an Apple iPhone's "Internal Storage" to a specified destination folder on your computer. It utilizes the win32com.shell library to interact with the Windows Shell, allowing the script to identify and move image files efficiently.

Features:
- Recursively moves all image files from the "Internal Storage" of your Apple iPhone to a designated folder on your computer. 
- Utilizes the Windows Shell for efficient file operations.
- Supports dynamic destination folder selection.

Prerequisites:
- Python: Ensure that you have Python installed on your system. You can download it from python.org.

Required Libraries:
- win32com: Install it using pip install pywin32.

Usage: 
Clone the Repository...
- git clone <repository-url>
- cd ios-photo-transfer-script

Run the Script...
- python ios_photo_transfer_script.py

Follow the Prompts...
- The script will prompt you to connect your iPhone, select the "Internal Storage" folder, and specify the destination folder on your computer.

Sit Back and Relax...
- The script will recursively move all image files to the designated destination folder.

Configuration:
- Destination Folder: You can modify the script to specify your preferred destination folder by updating the appropriate variables.

Cloud Storage (Optional):
- If you prefer to use a cloud storage solution, follow the instructions in the script comments to update the destination folder accordingly.

Notes:
- Ensure your iPhone is connected and recognized by the script.
- For cloud storage, configure the script to point to the local sync folder provided by the cloud service.

Contributors
- Rolando Fuentes (darkreconn)

License
- This project is licensed under the MIT License.
