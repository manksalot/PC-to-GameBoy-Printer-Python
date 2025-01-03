import serial
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from scipy import ndimage
from Send_Packet import send_packet
from Add_CheckSum import add_checksum
from AutoDetectCom import autodetectcom
from Image_Rectifier import image_rectifier

# PC to Game Boy printer, Caleb Dennis
# -------------------------------------------------------------
palette = 0xE4  # any value is possible
intensity = 0x7F  # 0x00->0x7F
PRNT_INI = [0x88, 0x33, 0x02, 0x00, 0x04, 0x00, 0x01, 0x00, palette, intensity]
serial_port = autodetectcom()  # enter your COM port here
margin = 3  # 0 before margin, 3 after margins, used between images
INIT = [0x88, 0x33, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00]  # INT command
INQU = [0x88, 0x33, 0x0F, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00]  # INQUIRY command
EMPT = [0x88, 0x33, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00]  # Empty data packet
DATA = [0x88, 0x33, 0x04, 0x00, 0x80, 0x02]  # DATA packet header
# --------------------------------------------------------------

def feed():    
    global PRNT_INI
    global serial_port
    global margin
    global INIT
    global INQU
    global EMPT
    global DATA
    serial_port = autodetectcom()  # enter your COM port here
    arduino_obj = serial.Serial(serial_port, 9600, timeout=255)
    time.sleep(2.5)  # allows the Arduino to reboot before sending data
    send_packet(arduino_obj, INIT)
    time.sleep(0.2)
    send_packet(arduino_obj, EMPT)
    print('Sending PRNT command with margin')
    PRNT_INI[7] = margin
    PRNT = add_checksum(PRNT_INI)
    send_packet(arduino_obj, PRNT)

    for i in range(10 * margin):
        time.sleep(0.1)
        send_packet(arduino_obj, INQU)
        
    PRNT_INI[7] = 0x00
    PRNT = add_checksum(PRNT_INI)
    time.sleep(0.1)
    arduino_obj.close()


# send and print image to gb printer program
def print_image(directory):
    global PRNT_INI
    global serial_port
    global INIT
    global INQU
    global EMPT
    global DATA
    print('-----------------------------------------------------------')
    print('           |Beware, this code is for Python|               ')
    print('-----------------------------------------------------------')

    PRNT = add_checksum(PRNT_INI)
    arduino_obj = serial.Serial(serial_port, 9600, timeout=255)
    time.sleep(2.5)  # allows the Arduino to reboot before sending data
    
    packets = 0
    currentfilename = directory
    print(f'Converting image {currentfilename} in progress...')
    # Using PIL for image processing
    img_path =currentfilename
    a = np.array(Image.open(img_path))

    # Check if image is indexed (palettized)
    if len(a.shape) == 2 and hasattr(Image.open(img_path), 'palette'):
        print('Indexed image, converting to grayscale')
        a = np.array(Image.open(img_path).convert('L'))

    height, width = a.shape[:2]
    layers = 1 if len(a.shape) == 2 else a.shape[2]

    if layers > 1:  # dealing with color images
        print('Color image, converting to grayscale')
        a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
        height, width = a.shape
        layers = 1

    C = np.unique(a)

    if len(C) <= 4 and height == 160:  # dealing with pixel perfect image, bad orientation
        print('Bad orientation, image rotated')
        a = ndimage.rotate(a, 270, reshape=True)
        height, width = a.shape

    if len(C) <= 4 and width != 160:  # dealing with pixel perfect upscaled/downscaled images
        print('Image is 2 bpp or less, which is good, but bad size: fixing it')
        scale_factor = 160/width
        a = cv2.resize(a, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)
        height, width = a.shape

    if len(C) > 4 or width != 160:  # dealing with 8-bit images in general
        print('8-bits image rectified and dithered with Bayer matrices')
        a = image_rectifier(a)
        height, width = a.shape

    if len(C) == 1:  # dealing with one color images
        print('Empty image -> neutralization, will print full white')
        a = np.zeros((height, width))

    if height % 16 != 0:  # Fixing images not multiple of 16 pixels
        print('Image height is not a multiple of 16 : fixing image')
        C = np.unique(a)
        new_lines = int(np.ceil(height/16)*16 - height)
        color_footer = float(C[-1])
        footer = np.ones((new_lines, width)) * color_footer
        a = np.vstack((a, footer))
        height, width = a.shape

    height, width = a.shape
    C = np.unique(a)
    print(f'Buffering image {currentfilename} into GB tile data...')
    
    if len(C) == 4:  # 4 colors, OK
        Black, Dgray, Lgray, White = C
    elif len(C) == 3:  # 3 colors, sacrifice LG (not well printed)
        Black, Dgray = C[:2]
        Lgray = None
        White = C[2]
    elif len(C) == 2:  # 2 colors, sacrifice LG and DG
        Black = C[0]
        Dgray = None
        Lgray = None
        White = C[1]

    hor_tile = width // 8
    vert_tile = height // 8
    tile = 0
    H = 0
    L = 0
    H_tile = 0
    L_tile = 0
    O = []
    y_graph = 0

    for x in range(hor_tile):
        for y in range(vert_tile):
            tile += 1
            b = a[H:H+8, L:L+8]
            for i in range(8):
                V1 = ['0'] * 8
                V2 = ['0'] * 8
                for j in range(8):
                    if b[i,j] == Lgray:
                        V1[j], V2[j] = '1', '0'
                    elif b[i,j] == Dgray:
                        V1[j], V2[j] = '0', '1'
                    elif b[i,j] == White:
                        V1[j], V2[j] = '0', '0'
                    elif b[i,j] == Black:
                        V1[j], V2[j] = '1', '1'
                O.extend([int(''.join(V1), 2), int(''.join(V2), 2)])

            if tile == 40:
                plt.cla()  # Clear the current axes
                plt.imshow(a, cmap='gray')
                plt.draw()  # Redraw the image without any rectangles
                rect = patches.Rectangle((1, y_graph), 160-1, 16, 
                                    edgecolor='r', facecolor='none', 
                                    linewidth=3)
                plt.gca().add_patch(rect)
                plt.draw()
                plt.pause(0.1)
                plt.draw()  # Update the plot after removing the rectangle
                DATA_READY = DATA + O
                DATA_READY = add_checksum(DATA_READY)
                packets += 1
                y_graph += 16
                print(f'Buffering DATA packet#{packets}')
                send_packet(arduino_obj, INIT)
                time.sleep(0.1)
                print(f'Sending DATA packet#{packets}')
                send_packet(arduino_obj, DATA_READY)
                send_packet(arduino_obj, EMPT)
                send_packet(arduino_obj, PRNT)
                
                for i in range(10 * margin): #TODO: change this to 10 if it doesn't work
                    time.sleep(0.1)
                    send_packet(arduino_obj, INQU)
                    
                time.sleep(0.1)
                O = []
                tile = 0
                
            L += 8
            L_tile += 1
            if L >= width:
                L = 0
                L_tile = 0
                H += 8
                H_tile += 1

    packets += 3

    send_packet(arduino_obj, INIT)
    time.sleep(0.2)
    send_packet(arduino_obj, EMPT)
    print('Sending PRNT command with margin')
    PRNT_INI[7] = margin
    PRNT = add_checksum(PRNT_INI)
    send_packet(arduino_obj, PRNT)

    for i in range(10 * margin):
        time.sleep(0.2)
        send_packet(arduino_obj, INQU)
        
    PRNT_INI[7] = 0x00
    PRNT = add_checksum(PRNT_INI)
    time.sleep(0.1)
    arduino_obj.close()

    # Close serial connection
    arduino_obj.close()
    print('End of printing')
    plt.close('all')