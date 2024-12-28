import numpy as np
from PIL import Image

def image_rectifier(image_non_rectified):
    Dithering_patterns = [0x2A, 0x5E, 0x9B, 0x51, 0x8B, 0xCA, 0x33, 0x69, 0xA6, 0x5A, 0x97, 0xD6,
                         0x44, 0x7C, 0xBA, 0x37, 0x6D, 0xAA, 0x4D, 0x87, 0xC6, 0x40, 0x78, 0xB6,
                         0x30, 0x65, 0xA2, 0x57, 0x93, 0xD2, 0x2D, 0x61, 0x9E, 0x54, 0x8F, 0xCE,
                         0x4A, 0x84, 0xC2, 0x3D, 0x74, 0xB2, 0x47, 0x80, 0xBE, 0x3A, 0x71, 0xAE]
    
    a = np.array(image_non_rectified)
    height, width = a.shape[:2]

    if height < width:
        a = np.rot90(a, k=3)
        height, width = a.shape[:2]

    # Resize image to 160px width
    new_height = int(height * (160 / width))
    a = Image.fromarray(a).resize((160, new_height), Image.BICUBIC)
    a = np.array(a)
    height, width = a.shape[:2]

    # Fix height to multiple of 16
    if height % 16 != 0:
        print('Image height is not a multiple of 16 : fixing image')
        new_lines = (((height + 15) // 16) * 16) - height
        footer = np.full((new_lines, width), 255, dtype=np.uint8)
        a = np.vstack((a, footer))
        height = a.shape[0]

    # 2D edge enhancement
    edge = a.astype(float)
    alpha = 0.5
    b = np.zeros_like(edge)
    for y in range(1, height-1):
        for x in range(1, width-1):
            b[y,x] = (4*edge[y,x] - edge[y-1,x] - edge[y+1,x] - 
                     edge[y,x-1] - edge[y,x+1]) * alpha
    
    a[:-1,:-1] = np.clip(a[:-1,:-1] + b[:-1,:-1], 0, 255).astype(np.uint8)

    # Bayer dithering matrices setup
    counter = 0
    Bayer_matDG_B = np.zeros((4,4))
    Bayer_matLG_DG = np.zeros((4,4))
    Bayer_matW_LG = np.zeros((4,4))
    
    for y in range(4):
        for x in range(4):
            Bayer_matDG_B[y,x] = Dithering_patterns[counter]
            counter += 1
            Bayer_matLG_DG[y,x] = Dithering_patterns[counter]
            counter += 1
            Bayer_matW_LG[y,x] = Dithering_patterns[counter]
            counter += 1

    # Create full-size dithering matrices
    Bayer_matDG_B_2D = np.tile(Bayer_matDG_B, (height//4 + 1, width//4 + 1))[:height,:width]
    Bayer_matLG_DG_2D = np.tile(Bayer_matLG_DG, (height//4 + 1, width//4 + 1))[:height,:width]
    Bayer_matW_LG_2D = np.tile(Bayer_matW_LG, (height//4 + 1, width//4 + 1))[:height,:width]

    # Apply dithering
    result = np.zeros_like(a)
    result[a < Bayer_matDG_B_2D] = 0
    result[(a >= Bayer_matDG_B_2D) & (a < Bayer_matLG_DG_2D)] = 80
    result[(a >= Bayer_matLG_DG_2D) & (a < Bayer_matW_LG_2D)] = 170
    result[a >= Bayer_matW_LG_2D] = 255

    return result