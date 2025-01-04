# PC-to-GameBoy-Printer-Python
Raphael Boichot's Matlab PC-to-Game-Boy-Printer interface converted to Python. With a few extras, I thought it would be more intuitive.

## Table of Contents
- [Running the Program](#running-the-program)
  - [Running in VS Code](#running-in-vs-code)
  - [Running as an EXE](#running-as-an-exe)
- [GUI Overview](#gui-overview)
- [Arduino Setup](#arduino-setup)
- [Visuals](#visuals)
- [Features](#features)
- [Contributing](#contributing)

## Running the Program

There are two ways to run the program: from the Python source code or as an executable (EXE).

### Running in VS Code
1. **Install Required Libraries**: Use the following command to install the necessary libraries. Note: this is in the Python-Support-files/Python-requirements.txt:
    ```bash
    pip install pyserial numpy pillow matplotlib opencv-python scipy pyinstaller
    ```
   **Run the Program**: Ensure all files are in the same directory and execute `PC_Gameboy_Printer.py` in VS Code. Remember to include the ICO file from the Python-Support-Files folder.

   **Note**: Include the ICO file from the Python-Support-Files folder in the same folder as the `.py` files.

### Running as an EXE
1. You must install PyInstaller by running this command:

    ```bash
    pip install pyinstaller
    ```

   **Note**: This should be included in the mentioned `.txt` file.

2. **Create the EXE**: In the same folder as the Python files, run:

    ```bash
    pyinstaller --onefile --icon=gameboy.ico --noconsole --add-data "gameboy.ico;." --add-data "Print_Image.py;." --add-data "Send_Packet.py;." --add-data "Add_CheckSum.py;." --add-data "AutoDetectCom.py;." --add-data "Image_Rectifier.py;." --hidden-import "scipy._lib.array_api_compat.numpy.fft" PC_Gameboy_Printer.py
    ```
    Note: This will generate a `dist` folder containing the EXE.
   
## GUI
This is the program's GUI. The program will start with a fixed window size and a blank spot above the GUI buttons.
The GUI window will automatically adjust the window size to the loaded picture.

![GUI](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/GUI.JPG)
*The program's GUI interface.*

-There are three options for the GUI buttons: loading the picture, feeding the paper, and printing the image.

While running the program, every time you click the feed or print button, it will auto-detect the COM the Arduino uses and create a serial connection.
It will also handle closing the COM port used. This ensures a clean disconnect and prevents erroring out or having a COM Port Leak.

When you start a print, another window displays a converted version of the selected image. This image has been resized and oriented to achieve the best ratio. Finally, a dithering process converts the image to hex data, which is stored and sent to the Arduino as packets. Each red rectangle represents a section of the image the printer is printing.

-Here is the image scan window.

![Scan Window](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/GUI-Scan-visual.JPG)

## Arduino Setup and Walkthrough.
For the Arduino, use the .ino file for the sketch code. This will be in the Arduino_Nano_GB_Printer_Interface. Folder inside the .ino that you will load into the Arduino Board.
-NOTE: this will work for both Nano and Uno boards, but you might have to change the SDA SCL pins if you want to use an OLED on a Uno. The OLED I use is a 128 x 32-pixel.

## Arduino Setup
-Here is the completed device. This has an Arduino Nano, a 128x32-pixel OLED, and a custom break-out board "BOB."

![Arduino PCB](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/Arduino-PCB.jpg)
*Arduino setup with a 128x32-pixel OLED and custom breakout board.*

![Arduino With ProtoCase](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/Angled-Shot-Protocase.jpg)
*Arduino setup with custom Resin printed case.*

## Visuals
-When the Arduino boots, you will see a booting screen and a standby screen indicating that the device is ready.

![Arduino Booting](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/Arduino-Booting.jpg)
*Arduino booting screen.*

![Arduino Standby](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/STBY1.jpg)
*Arduino standby screen.*

## Features
- Intuitive GUI for easy image loading and printing.
- Automatic COM port detection for seamless operation.
- Image conversion and dithering for optimal printing.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
