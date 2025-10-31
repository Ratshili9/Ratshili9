import cv2
import numpy as np
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_ui_elements(img):
    """
    Detect all UI elements using multiple strategies
    """
    elements = []
    
    # Multiple detection strategies
    elements.extend(detect_rectangles(img))
    elements.extend(detect_text_regions(img))
    elements.extend(detect_contours(img))
    
    # Remove duplicates and filter elements
    elements = filter_elements(elements, img.shape[1], img.shape[0])
    
    return elements

def detect_rectangles(img):
    """
    Detect rectangular UI elements
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    elements = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < 1000:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Filter unreasonable aspect ratios
        aspect_ratio = w / h if h > 0 else 0
        if aspect_ratio < 0.1 or aspect_ratio > 10:
            continue
        
        # Detect text in region
        roi = img[y:y+h, x:x+w]
        text_results = reader.readtext(roi, detail=0)
        detected_text = ' '.join(text_results).strip() if text_results else ''
        
        element_type = classify_rectangle(w, h, aspect_ratio, detected_text, area)
        
        elements.append({
            'id': f"rect_{i}",
            'type': element_type,
            'text': detected_text,
            'position': {'x': x, 'y': y, 'width': w, 'height': h}
        })
    
    return elements

def detect_text_regions(img):
    """
    Detect text regions using EasyOCR
    """
    results = reader.readtext(img)
    
    elements = []
    for i, (bbox, text, confidence) in enumerate(results):
        if confidence < 0.3:
            continue
            
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        
        x, y = top_left
        w = bottom_right[0] - top_left[0]
        h = bottom_right[1] - top_left[1]
        
        element_type = classify_text(text, w, h)
            
        elements.append({
            'id': f"text_{i}",
            'type': element_type,
            'text': text.strip(),
            'position': {'x': x, 'y': y, 'width': w, 'height': h},
            'confidence': confidence
        })
    
    return elements

def detect_contours(img):
    """
    Detect elements using contour detection
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    elements = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < 500:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        
        elements.append({
            'id': f"contour_{i}",
            'type': "container",
            'text': "",
            'position': {'x': x, 'y': y, 'width': w, 'height': h}
        })
    
    return elements

def classify_rectangle(width, height, aspect_ratio, text, area):
    """Classify rectangle-based elements"""
    if text:
        if 1.5 < aspect_ratio < 4 and height > 30:
            return "button"
        else:
            return "card"
    elif aspect_ratio > 4:
        return "input"
    else:
        return "container"

def classify_text(text, width, height):
    """Classify text elements"""
    if len(text) < 25 and text.strip().isupper():
        return "heading"
    elif any(keyword in text.lower() for keyword in ['button', 'click', 'submit']):
        return "button"
    else:
        return "text"

def filter_elements(elements, img_width, img_height):
    """Filter and clean detected elements"""
    filtered = []
    
    for element in elements:
        pos = element['position']
        
        # Skip very small elements
        if pos['width'] < 10 or pos['height'] < 10:
            continue
            
        # Skip elements mostly outside image
        if (pos['x'] > img_width * 0.9 or pos['y'] > img_height * 0.9):
            continue
            
        filtered.append(element)
    
    return filtered