# PC-to-GameBoy-Printer-Python

A Python interface for printing images using a Game Boy Printer, originally developed in Matlab by Raphael Boichot. This version includes additional features for improved usability.

## Table of Contents
- [Running the Program](#running-the-program)
  - [Running in VS Code](#running-in-vs-code)
  - [Running as an EXE](#running-as-an-exe)
- [GUI Overview](#gui-overview)
- [Arduino Setup](#arduino-setup)
- [Visuals](#visuals)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Running the Program

There are two ways to run the program: from the Python source code or as an executable (EXE).

### Running in VS Code
1. **Install Required Libraries**: Use the following command to install the necessary libraries:
    ```bash
    pip install pyserial numpy pillow matplotlib opencv-python scipy pyinstaller
    ```
2. **Run the Program**: Ensure all files are in the same directory and execute `PC_Gameboy_Printer.py` in VS Code. Remember to include the ICO file from the Python-Support-Files folder.

### Running as an EXE
1. **Install PyInstaller**: Run the command:
    ```bash
    pip install pyinstaller
    ```
2. **Create the EXE**: In the same folder as the Python files, run:
    ```bash
    pyinstaller --onefile --icon=gameboy.ico --noconsole --add-data "gameboy.ico;." --add-data "Print_Image.py;." --add-data "Send_Packet.py;." --add-data "Add_CheckSum.py;." --add-data "AutoDetectCom.py;." --add-data "Image_Rectifier.py;." --hidden-import "scipy._lib.array_api_compat.numpy.fft" PC_Gameboy_Printer.py
    ```
   This will generate a `dist` folder containing the EXE.

## GUI Overview

The GUI features a fixed window size that adjusts based on the loaded image. It includes buttons for loading pictures, feeding paper, and printing images. The program automatically detects the COM port for the Arduino and manages the serial connection.

![GUI](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/GUI.JPG)
*The program's GUI interface.*

## Arduino Setup

For the Arduino, use the provided `.ino` file located in the `Arduino_Nano_GB_Printer_Interface` folder. It is compatible with both Nano and Uno boards, but you may need to adjust the SDA and SCL pins for an OLED display on the Uno.

![Arduino PCB](https://github.com/AKABigDinner/PC-to-GameBoy-Printer-Python/blob/main/Photos/Arduino-PCB.jpg)
*Arduino setup with a 128x32-pixel OLED and custom breakout board.*

## Visuals

The project includes several images showcasing the GUI, the Arduino setup, and the device in operation.

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

## License
This project is licensed under the MIT License. See the LICENSE file for details.
