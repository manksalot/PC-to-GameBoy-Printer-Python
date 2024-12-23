import serial
from findPort import AutodetectCOM

arduino_obj = serial.Serial(AutodetectCOM(), baudrate=9600, timeout=255)

def send_packet(packet_TX):
    global arduino_obj
    if arduino_obj is None:
        print("Error: Arduino object is not initialized.")
        return  # Exit the function if arduino_obj is None

    for byte in packet_TX:
        arduino_obj.write(byte.to_bytes(1, 'big'))  # Send byte as uint8
        response = arduino_obj.read(1)  # Read response from the Arduino
        if response:
            print(f"Received response: {response[0]}")  # Print the response byte

def close_serial():
    global arduino_obj
    if arduino_obj is not None:
        print('Closing serial port')
        arduino_obj.flush()  # Flush the serial buffer
        arduino_obj.close()  # Close the serial connection
        arduino_obj = None  # Set the global variable to None
        print('End of printing')
    else:
        print('Serial port is already closed or was never opened.')