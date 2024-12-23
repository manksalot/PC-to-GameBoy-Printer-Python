import time
import numpy as np
from comControl import send_packet

def add_checksum(input_list):
    # Ensure input_list is a list
    if isinstance(input_list, np.ndarray):
        input_list = input_list.tolist()  # Convert NumPy array to list if necessary

    # Calculate the checksum from the 3rd element to the end
    checksum = sum(input_list[2:])  # Sums from the 3rd element onward
    # Calculate LSB and MSB
    LSB = checksum % 256  # Least Significant Byte
    MSB = (checksum // 256) % 256  # Most Significant Byte
    # Create the output list
    output = input_list + [LSB, MSB, 0, 0]  # Concatenate the checksum bytes
    return output

def Feed():
    ##-------------------------------------------------------------
    palette=0xE4 ##any value is possible
    intensity=0x7F ##0x00->0x7F
    PRNT_INI = [0x88, 0x33, 0x02, 0x00, 0x04, 0x00, 0x01, 0x00, palette, intensity] ##, 0x2B, 0x01, 0x00, 0x00}; %PRINT without feed lines, default
    margin=3 ##0 before margin, 3 after margins, used between images
    INIT = [0x88, 0x33, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00] ##INT command
    INQU = [0x88, 0x33, 0x0F, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00] ##INQUIRY command
    EMPT = [0x88, 0x33, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00] ##Empty data packet, mandatory for validate DATA packet
    ##--------------------------------------------------------------

    # --------- Printing loop -----------------------------
    send_packet(INIT)
    time.sleep(0.1)
    send_packet(EMPT)  # Mandatory in the protocol
    print('Sending PRNT command with margin')
    
    PRNT_INI[7] = margin  # Prepare PRINT command with margin (index 7 for 8th element)
    PRNT = add_checksum(PRNT_INI)
    send_packet(PRNT)

    for i in range(10 * margin):
        time.sleep(0.1)  # Time for the printer head to print one line of 16 pixels
        send_packet(INQU)

    PRNT_INI[7] = 0x00  # Restore PRINT command without margin for next image
    PRNT = add_checksum(PRNT_INI)
    time.sleep(0.1)
    # ---------------------------------------------------

def printdata(DATA_READY, packet):
    ##-------------------------------------------------------------
    palette=0xE4 ##any value is possible
    intensity=0x7F ##0x00->0x7F
    PRNT_INI = [0x88, 0x33, 0x02, 0x00, 0x04, 0x00, 0x01, 0x00, palette, intensity] ##, 0x2B, 0x01, 0x00, 0x00}; %PRINT without feed lines, default
    margin=3 ##0 before margin, 3 after margins, used between images
    INIT = [0x88, 0x33, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00] ##INT command
    INQU = [0x88, 0x33, 0x0F, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00] ##INQUIRY command
    EMPT = [0x88, 0x33, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00] ##Empty data packet, mandatory for validate DATA packet
    ##--------------------------------------------------------------
    PRNT = add_checksum(PRNT_INI)
    print(f"Sending packet: {packet}")
    # Main printing loop
    send_packet(INIT)
    time.sleep(0.1)  # Skip the first packet without processing
    packets = 1  # Example packet number, adjust as needed
    print(f'Sending DATA packet#{packets}')
    send_packet(DATA_READY)
    send_packet(EMPT)  # Mandatory in the protocol
    send_packet(PRNT)
    for i in range(10):
        time.sleep(0.1)  # Time for the printer head to print one line of 16 pixels
        send_packet(INQU)
    time.sleep(0.1)  # Final pause
