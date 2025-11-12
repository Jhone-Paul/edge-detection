import sys
from PIL import Image
from numpy import asarray
import numpy as np 
import matplotlib.pyplot as plt
# rgb cus who gaf abt grayscale
# also looping over all pixels is dumb and so i used vectorized numpy shit 
def sobel_rgb(image, Gx, Gy):
    h, w = len(image), len(image[0])
    print(f"{h} image {w}")
    
    image = image.astype(np.float32)
    
    results = np.zeros_like(image)
    
    # one for each channel
    for c in range(3):
        channel = image[:, :, c]
        

        gx = np.zeros_like(channel)
        gy = np.zeros_like(channel)
        
        for ky in range(3):
            for kx in range(3):
                # kernel offset
                y_start, y_end = ky, h - (2 - ky)
                x_start, x_end = kx, w - (2 - kx)
                
                gx[1:h-1, 1:w-1] += channel[y_start:y_end, x_start:x_end] * Gx[ky][kx]
                gy[1:h-1, 1:w-1] += channel[y_start:y_end, x_start:x_end] * Gy[ky][kx]

        magnitude = np.sqrt(gx**2 + gy**2)
        results[:, :, c] = np.clip(magnitude, 0, 255)
    
    return results.astype(np.uint8)

def main(args):

    img = Image.open('Sample.jpg')
    a = asarray(img)
    print(type(a))
    print(a.shape)

    # sobel kernels
    Gx = [[-1,0,1],
          [-2,0,2],
         [-1,0,1]]
    Gy = [[1,2,1],
          [0,0,0],
        [-1,-2,-1]]

    print(a[0][0][0])

    if not (len(args) > 0):
        print("defaulting to a sample image and sobel operator")
    else:
        try:
            imgpath = args[0]
            img = Image.open(imgpath)
            a = asarray(img)
        except Exception as e:
            print(f"path dont work or summin {e}")
            pass
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    edges = sobel_rgb(a, Gx,Gy)
    # OG
    axes[0].imshow(a)
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    # EdGe(EG)
    axes[1].imshow(edges)
    axes[1].set_title('Sobel Edges (RGB)')
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    args = sys.argv
    main(args)
