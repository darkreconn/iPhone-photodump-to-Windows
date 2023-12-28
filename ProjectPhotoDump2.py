from win32com.shell import shell, shellcon
import pythoncom

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

# folder where source file is located
for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "201207__":
        pidl_get = pidl
        break
folderPIDL = pidl_get
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

# imgPIDL: PIDL of the source file
for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "IMG_0039.JPG":
        imgPIDL = pidl

###TS-PASS###
print(f"pidl: {imgPIDL}")
###TS-PASS###

# Then, get the ShellObject of Destination folder (C:\iOS-Photodumping)
        
###########################Attempt 1 with error (cant locate C drive)###########################
#for pidl in desktop:
#    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
#        pidl_dst = pidl
#        break
#dstFolder = desktop.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
#
#for pidl in dstFolder:
#    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "OS":
#        pidl_dst = pidl
#        break
#dstFolder = folder.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
#
#for pidl in dstFolder:
#    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "iOS-Photodumping":
#        pidl_dst = pidl
#        break
#dstFolder = folder.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
###########################End of Attempt 1###########################
        
###########################Attempt 2###########################
# Assuming 'desktop' is the IShellFolder object for the desktop
desktop = shell.SHGetDesktopFolder()

# Step 1: Get the IShellFolder for "This PC"
pidl_this_pc = None
for pidl in desktop:
    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
        pidl_this_pc = pidl
        break

folder_this_pc = desktop.BindToObject(pidl_this_pc, None, shell.IID_IShellFolder)

####TS####
print(f"pidl_this_pc: {pidl_this_pc}")
####TS####

# Step 2: Get the IShellFolder for "OS"
pidl_os = None
for pidl in folder_this_pc:
    print(f"Display Name: {folder_this_pc.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL)}")

    if folder_this_pc.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "OS (C:)":
        pidl_os = pidl
        break

####TS####
print(f"pidl_os: {pidl_os}")
if pidl_os is None:
    print("Error: Folder 'OS' not found.")
####TS####

folder_os = folder_this_pc.BindToObject(pidl_os, None, shell.IID_IShellFolder)

# Step 3: Get the IShellFolder for "iOS-Photodumping"
pidl_ios_photodumping = None
for pidl in folder_os:
    if folder_os.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "iOS-Photodumping":
        pidl_ios_photodumping = pidl
        break

####TS####
print(f"pidl_ios_photodumping: {pidl_ios_photodumping}")
####TS####

folder_ios_photodumping = folder_os.BindToObject(pidl_ios_photodumping, None, shell.IID_IShellFolder)

# Now, folder_ios_photodumping should be the IShellFolder for "C:\iOS-Photodumping"
###########################End of Attempt 2###########################

# Grab the PIDL from the folder object
fidl = shell.SHGetIDListFromObject(folder)
didl = shell.SHGetIDListFromObject(folder_ios_photodumping)

# Create a ShellItem of the source file
si = shell.SHCreateShellItem(fidl, None, imgPIDL) 
dst = shell.SHCreateItemFromIDList(didl)

# Python IFileOperation
pfo = pythoncom.CoCreateInstance(shell.CLSID_FileOperation,None,pythoncom.CLSCTX_ALL,shell.IID_IFileOperation)
pfo.SetOperationFlags(shellcon.FOF_NOCONFIRMATION)
pfo.CopyItem(si, dst, None) # Schedule an operation to be performed
success = pfo.PerformOperations() #perform operation

# Check if the operation was successful
print(f"Operation ran with following errors: {success}")

############ NEXT VERSION TO INCLUDE: #################
# Improve success message to be more detailed
# Targeting all files in the folder, and all folders in Apple Iphone internal storage
# Prevent duplicate folders/files in the future
# Automation of the operation as soon as the iPhone is connected including a permission prompt to continue running