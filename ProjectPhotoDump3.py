from win32com.shell import shell, shellcon
import pythoncom

# Function to recursively process folders and move files
def move_files_in_folder(src_folder, dst_folder):
    # Iterate through files in the source folder
    for pidl_file in src_folder:
        # Get the PIDL of each file in the folder
        imgPIDL = pidl_file

        # Grab the PIDL from the folder object
        fidl = shell.SHGetIDListFromObject(src_folder)
        didl = shell.SHGetIDListFromObject(dst_folder)

        # Create a ShellItem of the source file
        si = shell.SHCreateShellItem(fidl, None, imgPIDL)
        dst = shell.SHCreateItemFromIDList(didl)

        # Python IFileOperation
        pfo = pythoncom.CoCreateInstance(shell.CLSID_FileOperation, None, pythoncom.CLSCTX_ALL, shell.IID_IFileOperation)
        pfo.SetOperationFlags(shellcon.FOF_NOCONFIRMATION)
        pfo.CopyItem(si, dst, None)  # Schedule an operation to be performed
        success = pfo.PerformOperations()  # Perform operation

        # Check if the operation was successful
        print(f"Operation ran with following errors: {success}")

    # Iterate through subfolders in the source folder
    for pidl_subfolder in src_folder:
        # Get the ShellObject of the subfolder
        subfolder = src_folder.BindToObject(pidl_subfolder, None, shell.IID_IShellFolder)

        # Recursively move files in the subfolder
        move_files_in_folder(subfolder, dst_folder)

# get the PIDL of source file and the ShellObject of the folder in which source file is located
# and the PIDL of the folder
desktop = shell.SHGetDesktopFolder()
for pidl in desktop:
    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
        pidl_get = pidl
        break
folder = desktop.BindToObject(pidl_get, None, shell.IID_IShellFolder)

for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Apple iPhone":
        pidl_get = pidl
        break
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Internal Storage":
        pidl_get = pidl
        break
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

# Destination folder (D:\iOS-Photodumping)
# Assuming 'desktop' is the IShellFolder object for the desktop
desktop = shell.SHGetDesktopFolder()

# Step 1: Get the IShellFolder for "This PC"
pidl_this_pc = None
for pidl in desktop:
    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
        pidl_this_pc = pidl
        break

folder_this_pc = desktop.BindToObject(pidl_this_pc, None, shell.IID_IShellFolder)

# Step 2: Get the IShellFolder for "image bus (D:)"
pidl_os = None
for pidl in folder_this_pc:
    if folder_this_pc.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "image bus (D:)":
        pidl_os = pidl
        break

if pidl_os is None:
    print("Error: Folder 'image bus drive' not found.")
else:
    folder_os = folder_this_pc.BindToObject(pidl_os, None, shell.IID_IShellFolder)

    # Step 3: Get the IShellFolder for "iOS-Photodumping"
    pidl_ios_photodumping = None
    for pidl in folder_os:
        if folder_os.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "iOS-Photodumping":
            pidl_ios_photodumping = pidl
            break

    if pidl_ios_photodumping is None:
        print("Error: Folder 'iOS-Photodumping' not found.")
    else:
        folder_ios_photodumping = folder_os.BindToObject(pidl_ios_photodumping, None, shell.IID_IShellFolder)

        # Now, folder_ios_photodumping should be the IShellFolder for "D:\iOS-Photodumping"

        # Move files in Internal Storage to iOS-Photodumping
        move_files_in_folder(folder, folder_ios_photodumping)
