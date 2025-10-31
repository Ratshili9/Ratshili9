# 🖼️ Screenshot to Code Converter

## Hi there 👋 

This project converts UI screenshots into functional HTML/CSS code using computer vision and machine learning techniques.

## 🚀 What This Project Does

This project is designed to convert UI screenshots into HTML/CSS code. It uses image recognition and machine learning to identify the various elements of a user interface and generates clean, responsive code.

### How It Works:
- **Image Processing**: Analyzing the screenshot to detect elements like buttons, text, images, and layout structures
- **Machine Learning**: Using models to classify and generate HTML/CSS based on what it recognizes in the image  
- **Front-End Code Generation**: Translating the detected elements into structured HTML and styled CSS

## 🛠️ Tech Stack

- **Backend**: Flask, Python
- **Computer Vision**: OpenCV, NumPy
- **OCR**: EasyOCR for text extraction
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Werkzeug

## 📁 Project Structure

screenshot-to-code/
├── app.py # Main Flask application
├── image_processor.py # Image processing pipeline
├── element_detector.py # UI element detection logic
├── html_generator.py # HTML/CSS code generation
├── requirements.txt # Dependencies
├── static/ # Frontend assets
│ ├── css/
│ ├── js/
│ └── uploads/
└── templates/ # HTML templates
└── index.html


## 🎯 Features

- **Automated UI Detection**: Identifies buttons, inputs, text elements, and containers
- **Text Extraction**: Uses OCR to extract and preserve text content
- **Smart Classification**: Machine learning-inspired element classification
- **Responsive HTML Generation**: Produces clean, styled HTML/CSS code
- **RESTful API**: Easy integration with frontend applications

## 🚀 Getting Started

### Installation & Usage

```bash
# Clone repository
git clone https://github.com/Ratshili9/screenshot-to-code.git

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Visit http://localhost:5000