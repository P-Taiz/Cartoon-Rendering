import cv2
import numpy as np
import os

def render_cartoon(image_path, output_path=None):

    # Read the input image
    img = cv2.imread(image_path)
    
    # Check if image is loaded successfully
    if img is None:
        raise ValueError(f"Unable to read image from {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur to reduce noise
    gray = cv2.medianBlur(gray, 5)
    
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(
        gray, 
        255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        9, 
        9
    )
    
    # Apply bilateral filter to preserve edges while smoothing color
    color = cv2.bilateralFilter(img, 9, 300, 300)
    
    # Combine color image with edges mask
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    # Save output image if path is provided
    if output_path:
        cv2.imwrite(output_path, cartoon)
    
    return cartoon

def main():
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    input_images = [
        "input/Faker.jpeg",
        "input/japan.jpg",
        "input/OIP.jpeg"
    ]
    
    for idx, image_path in enumerate(input_images):
        try:
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_folder, f'cartoon_{idx+1}_{filename}')
            render_cartoon(image_path, output_path)
            print(f"Processed: {image_path} -> {output_path}")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

if __name__ == '__main__':
    main()