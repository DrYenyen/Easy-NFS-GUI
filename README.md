# Easy-NFS-GUI
A GUI to help setup a Windows NFS for use with Itemzflow.
Most of the source code for this came from my other GUI for PPPwn. 
And it is as always open source this time it compiles and releases through github since i only need to release the exe.
Press on "More Info" if windows flags it as an unrecognised app the "Run anyway"

# Instructions  
1. The GUI needs this NFS server https://github.com/winnfsd/winnfsd/releases/tag/2.4.0 in the same directory as it. 
2. Open the GUI and set the share folder (for example D:\PS4\Games) and your IP by reading your current IP or using the IP info button to view all IP info then press the "Run NFS server" button. 
3. Back on your PS4 make sure it is currently exploited.
4. Connect to the same network as your PC.
5. Launch Itemzflow and after the "download covers" prompt (if you haven't disabled it) press "Options" on your controller.
6. In Itemzflow settings locate and select "Fuse NFS IP".
7. There input your PC/Server IP address and press R2 for example: 192.168.1.14
* To only access specific subfolders you can do so when you Fuse the NFS IP in itemzflow for example: nfs://192.168.1.14/fpkgs
* This will give you access to the following sample path D:\PS4\Games\fpkgs
8. For more instructions and connection settings see https://consolemods.org/wiki/PS4:How_to_install_PKG_files

# To do 
1. Make the GUI create a batch file for future use when the directory and IP don't need to be changed.
