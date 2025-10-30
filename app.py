from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import easyocr
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])


def process_ui_layout(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert to gray for detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges
    edges = cv2.Canny(blurred, 30, 150)

    # Find contours
    contours, _ = cv2.findContours(
        edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    html_output = "<div class='generated-box'>\n"

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Skip small elements
        if w < 40 or h < 20:
            continue

        roi = img[y:y+h, x:x+w]
        text = reader.readtext(roi, detail=0)

        # Use text if detected, else describe as a box
        if text:
            html_output += f"  <p>{' '.join(text)}</p>\n"
        else:
            html_output += f"  <div style='width:{w}px; height:{h}px; border:1px solid #aaa;'></div>\n"

    html_output += "</div>"
    return html_output


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_code():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    html_code = process_ui_layout(file_path)

    return jsonify({'html_code': html_code})


if __name__ == '__main__':
    app.run(debug=True)
