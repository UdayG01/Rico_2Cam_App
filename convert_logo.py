import cv2
import numpy as np

def convert_logo():
    img_path = 'logo-Renata-IoT_1_new2-768x256.png'
    out_path = 'logo-Renata-IoT_1_new2_darkmode.png'
    
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Failed to load image")
        return
        
    print(f"Loaded image with shape: {img.shape}")
    
    # If image has an alpha channel
    if img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
        # Find dark pixels (text is usually near black)
        # thresholding: anything below 80 in all rgb channels
        dark_mask = (b < 100) & (g < 100) & (r < 100) & (a > 50)
        
        # Change dark pixels to white
        b[dark_mask] = 255
        g[dark_mask] = 255
        r[dark_mask] = 255
        
        img_out = cv2.merge((b, g, r, a))
        cv2.imwrite(out_path, img_out)
        print("wrestled a dark mode logo!")
        
convert_logo()
