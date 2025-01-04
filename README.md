# PC-to-GameBoy-Printer-Python
Raphael Boichot's Matlab PC-to-Game-Boy-Printer interface converted to Python.

## Running the Program
There are two ways to run the program: from the Python source code or as an EXE.

### Running in VS Code
1. First, you must install all the libraries needed for the program. The Python-Support-Files folder contains a `.txt` file with the pip install command for all the required libraries, or you can copy this command:

    ```bash
    pip install pyserial numpy pillow matplotlib opencv-python scipy pyinstaller
    ```

2. You can run this in VS Code. With all the files from the Python folder in the same directory, run `PC_Gameboy_Printer.py`.

   **Note**: Make sure to include the ICO file from the Python-Support-Files folder in the same folder as the `.py` files.

### Running as an EXE
1. You must install PyInstaller by running this command:

    ```bash
    pip install pyinstaller
    ```

   **Note**: This should be included in the mentioned `.txt` file.

2. Next, you need to run the following command while using VS Code and in the same folder as the Python files:

    ```bash
    pyinstaller --onefile --icon=gameboy.ico --noconsole --add-data "gameboy.ico;." --add-data "Print_Image.py;." --add-data "Send_Packet.py;." --add-data "Add_CheckSum.py;." --add-data "AutoDetectCom.py;." --add-data "Image_Rectifier.py;." --hidden-import "scipy._lib.array_api_compat.numpy.fft" PC_Gameboy_Printer.py
    ```

## GUI
![GUI](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/GUI.JPG)
