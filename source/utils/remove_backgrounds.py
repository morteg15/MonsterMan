import cv2
import numpy as np
from rembg import remove

def remove_background(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image is loaded properly
    if image is None:
        print("Error: Could not read the image.")
        return
    
    # Remove the background
    result = remove(image)
    
    # Save the output image
    cv2.imwrite(output_path, result)
    print(f"Background removed and saved to {output_path}")

# Example usage
remove_background('image.png', 'image.png')
