# PC-to-GameBoy-Printer-Python
Raphael-Boichot Matlab PC-to-Game-Boy-Printer-interface converted to Python

## Running the program
There are two ways to run the program. 
From the Python source code or as an EXE.

# Running in VS Code
In Python, you must install all the libraries needed for the program.
The Python-Support-Files has a .txt file with the pip install command for all the required libraries.
You can run this in VS Code. With all the files from the Python folder in the same directory, run PC_Gameboy_Printer.py.

Note: Make sure to include the ICO file from the Python-Support-Files folder in the same folder as the .py files.

# Running as an EXE
You must install pyinstaller by running this command: "pip install pyinstaller".
Note: this should be included in the mentioned .txt
Next, you need to run this next command while using VS Code and in the same folder as the Python files.
'''
pyinstaller --onefile --icon=gameboy.ico --noconsole --add-data "gameboy.ico;." --add-data "Print_Image.py;." --add-data "Send_Packet.py;." --add-data "Add_CheckSum.py;." --add-data "AutoDetectCom.py;." --add-data "Image_Rectifier.py;." --hidden-import "scipy._lib.array_api_compat.numpy.fft" PC_Gameboy_Printer.py'''


## GUI
![GUI](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/GUI.JPG)
