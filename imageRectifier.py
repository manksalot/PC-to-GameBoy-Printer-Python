import numpy as np
import cv2

def image_rectifier(image_non_rectified):
    # Dithering patterns
    Dithering_patterns = [
        0x2A, 0x5E, 0x9B, 0x51, 0x8B, 0xCA, 0x33, 0x69,
        0xA6, 0x5A, 0x97, 0xD6, 0x44, 0x7C, 0xBA, 0x37,
        0x6D, 0xAA, 0x4D, 0x87, 0xC6, 0x40, 0x78, 0xB6,
        0x30, 0x65, 0xA2, 0x57, 0x93, 0xD2, 0x2D, 0x61,
        0x9E, 0x54, 0x8F, 0xCE, 0x4A, 0x84, 0xC2, 0x3D,
        0x74, 0xB2, 0x47, 0x80, 0xBE, 0x3A, 0x71, 0xAE
    ]
    a = image_non_rectified  # create local variable
    height, width = a.shape  # Get the dimensions

    # Rotate the image if height is less than width
    if height < width:
        a = cv2.rotate(a, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate 90 degrees counter-clockwise to achieve 270 degrees

    # Check if height is not a multiple of 16
    if height % 16 != 0:  # Equivalent to not(rem(height, 16) == 0)
        print('Image height is not a multiple of 16: fixing image')
        new_lines = (height // 16 + 1) * 16 - height  # Calculate the number of new lines needed
        color_footer = 255  # White color for the footer
        footer = np.full((new_lines, width), color_footer, dtype=np.uint8)  # Create footer
        a = np.vstack((a, footer))  # Append footer to the image
        height, width = a.shape  # Update dimensions

    ## 2D edge enhancement
    edge = a.astype(np.float32)  # Equivalent to edge = double(a);
    alpha = 0.5
    b = np.zeros_like(edge)  # Initialize b with the same shape as edge (and a)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            b[y, x] = (4 * edge[y, x] - edge[y - 1, x] - edge[y + 1, x ] - edge[y, x - 1] - edge[y, x + 1]) * alpha

    a = np.clip(a.astype(np.float32) + b, 0, 255).astype(np.uint8)  # Update a with the edge enhancement

    # Initialize Bayer matrices
    Bayer_matDG_B = np.zeros((4, 4), dtype=np.uint8)  # 4x4 matrix
    Bayer_matLG_DG = np.zeros((4, 4), dtype=np.uint8)  # 4x4 matrix
    Bayer_matW_LG = np.zeros((4, 4), dtype=np.uint8)   # 4x4 matrix

    counter = 0
    for y in range(4):
        for x in range(4):
            Bayer_matDG_B[y, x] = Dithering_patterns[counter]
            counter += 1
            Bayer_matLG_DG[y, x] = Dithering_patterns[counter]
            counter += 1
            Bayer_matW_LG[y, x] = Dithering_patterns[counter]
            counter += 1

    # Initialize larger 2D matrices for Bayer dithering
    Bayer_matDG_B_2D = np.zeros((height, width), dtype=np.uint8)  # Adjust size as needed
    Bayer_matLG_DG_2D = np.zeros((height, width), dtype=np.uint8)  # Adjust size as needed
    Bayer_matW_LG_2D = np.zeros((height, width), dtype=np.uint8)   # Adjust size as needed

    for y in range(0, height, 4):  # Start from 0 and step by 4
        for x in range(0, width, 4):
            Bayer_matDG_B_2D[y:y+4, x:x+4] = Bayer_matDG_B
            Bayer_matLG_DG_2D[y:y+4, x:x+4] = Bayer_matLG_DG
            Bayer_matW_LG_2D[y:y+4, x:x+4] = Bayer_matW_LG

    for y in range(height):  # Loop through each pixel
        for x in range(width):

            pixel = a[y, x]  # Access the pixel value (an array of shape (3,))

            # Initialize pixel_out for each channel
            pixel_out = np.zeros(1, dtype=np.uint8)
            
            #for channel in range(3):  # Loop through each channel (R, G, B)
            if pixel < Bayer_matDG_B_2D[y, x]:
                pixel_out = 0
            elif pixel < Bayer_matLG_DG_2D[y, x]:
                pixel_out = 80
            elif pixel < Bayer_matW_LG_2D[y, x]:
                pixel_out = 170
            else:
                pixel_out = 255
            
            a[y, x] = pixel_out  # Update the pixel value in the original array a

    image_rectified = a  # Assign the array a to image_rectified
    return image_rectified

