import cv2
import numpy as np
from element_detector import detect_ui_elements
from html_generator import generate_complete_html

def process_ui_layout(image_path):
    """
    Main function to process image and generate UI layout
    """
    # Read and validate image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")

    height, width = img.shape[:2]
    
    # Detect UI elements
    elements = detect_ui_elements(img)
    
    # Generate HTML
    html_output = generate_complete_html(elements, width, height)
    
    return {
        'html': html_output,
        'elements': elements,
        'image_dimensions': {'width': width, 'height': height}
    }

def preprocess_image(img):
    """
    Preprocess image for better element detection
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred