from ultralytics import YOLO
import cv2  # For reading images
import os  # For handling file paths

# Load the YOLO v8 model with the trained 'best.pt'
model = YOLO('best.pt')  

# Function to detect fabric defects and determine if any defects are detected
def detect_fabric_defects(image_path):
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Perform detection with the YOLO model
    results = model.predict(image)  # Apply the model to the image

    # Check if any defects are detected (i.e., if there are any bounding boxes)
    defects_detected = any(results[0].boxes)  # True if there's at least one bounding box

    return defects_detected

# Test the function with a sample image
if __name__ == '__main__':
    sample_image_path = 't4.jpeg'  # Replace with your image path
   
    # Detect defects
    defects = detect_fabric_defects(sample_image_path)

    # Print the result
    if defects:
        print("Defects detected.")
    else:
        print("No defects detected.")
