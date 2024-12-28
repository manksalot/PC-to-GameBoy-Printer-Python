import serial.tools.list_ports

def autodetectcom():
    ports = serial.tools.list_ports.comports()# List all serial ports
    for port in ports:# Iterate through the list of ports
        # first if will find any arduino nano
        if 'CH340' in port.description: # Check if 'CH340' is in the port description
            return port.device  # Return the device name (e.g., 'COM3' or '/dev/ttyUSB0')
        # elif will find any arduino Uno
        elif 'Uno' in port.description:
            return port.device
    return None  # Return None if no CH340 port is found