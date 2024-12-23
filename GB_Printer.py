import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from comControl import close_serial
from sendCommand import Feed, printdata, add_checksum
from imageRectifier import image_rectifier

image_file = 'output.png'

def imagesc(a):
    global y_graph
    plt.imshow(a, cmap='gray')
    plt.axis('off')
    plt.gca().add_patch(patches.Rectangle((1, y_graph), 160 - 1, 16, edgecolor='red', linewidth=1, facecolor=(1, 0, 0)))
    plt.draw()
    plt.pause(.001)  # Update the plot
    y_graph += 16

def main():
    global y_graph
    DATA = [0x88, 0x33, 0x04, 0x00, 0x80, 0x02] ##DATA packet header, considering 640 bytes length by defaut (80 02), the footer is calculated onboard
    time.sleep(2.5)
    packets=0
    DATA_BUFFER=[]
    print(f'Converting image: {image_file}')
    a = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)

    if a is not None:
        # Check the number of channels
        if len(a.shape) == 2:  # Single channel (grayscale)
            print('Image is already grayscale.')
        elif len(a.shape) == 3:  # Color image
            print('Color image, converting to grayscale')
            a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        else:
            raise ValueError('Unexpected image format.')

    height, width = a.shape

    C = np.unique(a)

    if len(C) <= 4 and height == 160:  # dealing with pixel perfect image, bad orientation
        print('Bad orientation, image rotated')
        a = cv2.rotate(a, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate the image 270 degrees
        height, width = a.shape  # Update height and width after rotation

    if len(C) <= 4 and width != 160:  # dealing with pixel perfect upscaled/downscaled images
        print('Image is 2 bpp or less, which is good, but bad size: fixing it')
        a = cv2.resize(a, (160, height), interpolation=cv2.INTER_NEAREST)  # Resize the image to width 160
        height, width = a.shape  # Update height and width after resizing
        
    if len(C) > 4 or width != 160:  # dealing with 8-bit images in general
        print('8-bits image rectified and dithered with Bayer matrices')
        a = image_rectifier(a)  # Call the custom function to rectify the image
        height, width = a.shape  # Update height and width after rectification

    if len(C) == 1:  # dealing with one color images
        print('Empty image -> neutralization, will print full white')
        a = np.ones((height, width), dtype=np.uint8) * 255  # Create a full white image

    if height % 16 != 0:  # Fixing images not multiple of 16 pixels
        print('Image height is not a multiple of 16: fixing image')
        C = np.unique(a)
        new_lines = (height // 16 + 1) * 16 - height  # Calculate the number of new lines needed
        color_footer = float(C[-1])  # Get the last unique color value
        footer = np.full((new_lines, width), color_footer, dtype=np.uint8)  # Create footer with the last color
        a = np.vstack((a, footer))  # Append the footer to the original image
        height, width = a.shape  # Update height and width after adding footer

    # Get the dimensions of the image
    height, width = a.shape  # For grayscale images, layers will be 1


    # Get unique values in the image
    C = np.unique(a)

    # Print buffering message
    print(f'Buffering image {image_file} into GB tile data...')

    if len(C) == 4:  # 4 colors, OK
        Black = C[0]
        Dgray = C[1]
        Lgray = C[2]
        White = C[3]
    elif len(C) == 3:  # 3 colors, sacrifice LG (not well printed)
        Black = C[0]
        Dgray = C[1]
        Lgray = None  # Equivalent to an empty array in MATLAB
        White = C[2]
    elif len(C) == 2:  # 2 colors, sacrifice LG and DG
        Black = C[0]
        Dgray = None  # Equivalent to an empty array in MATLAB
        Lgray = None  # Equivalent to an empty array in MATLAB
        White = C[1]
    else:
        raise ValueError('Invalid number of colors. Expected 2, 3, or 4 colors.')

    # Calculate the number of horizontal and vertical tiles
    hor_tile = width / 8
    vert_tile = height / 8

    # Initialize other variables
    tile = 0
    H = 0
    L = 0
    H_tile = 1
    L_tile = 1
    V1 = ['0'] * 8  # Initialize V1 with '0's
    V2 = ['0'] * 8  # Initialize V2 with '0's
    O = []  # This will be an empty list
    y_graph = 0
    total_tiles = hor_tile * vert_tile
    for x in range(1, int(hor_tile) + 1):  # Iterate from 1 to hor_tile (inclusive)
        print(x)
        for y in range(1, int(vert_tile) + 1):  # Iterate from 1 to vert_tile (inclusive)
            print(y)
            #input("wait")
            tile += 1  # Increment the tile counter
            b = a[H:H+8, L:L+8]  # Extract a 8x8 tile from the image
            # Iterate over the 8x8 tile
            for i in range(8):
                for j in range(8):
                    if b[i, j] == Lgray:
                        V1[j] = '1'
                        V2[j] = '0'
                    elif b[i, j] == Dgray:
                        V1[j] = '0'
                        V2[j] = '1'
                    elif b[i, j] == White:
                        V1[j] = '0'
                        V2[j] = '0'
                    elif b[i, j] == Black:
                        V1[j] = '1'
                        V2[j] = '1'
                # Convert binary strings V1 and V2 to decimal and append to O
                O.append(int(''.join(V1), 2))  # Convert V1 from binary to decimal and append
                O.append(int(''.join(V2), 2))  # Convert V2 from binary to decimal and append
            if tile == 40:
                imagesc(a)
                DATA_READY = np.concatenate((DATA, O))
                DATA_READY = add_checksum(DATA_READY)
                packets=packets+1
                print(f"Buffering DATA packet# {packets}")
                printdata(DATA_READY, packets)
                O = []
                tile = 0
            L += 8  # Increment L by 8
            L_tile += 1  # Increment L_tile by 1
            if L >= width:
                L = 1  # Reset L to 1 to start from the first column
                L_tile = 1  # Reset L_tile to 1 for the new row
                H += 8  # Increment H to move to the next row of tiles
                H_tile += 1  # Increment H_tile by 1
    packets += 3
    imagesc(a)
    Feed()

main()
close_serial()