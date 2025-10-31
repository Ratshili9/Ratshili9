def generate_complete_html(elements, width, height):
    """
    Generate complete HTML from detected elements
    """
    if not elements:
        return generate_fallback_html()
    
    html_elements = generate_html_elements(elements, width, height)
    css_styles = generate_css_styles()
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Generated UI</title>
    <style>
{css_styles}
    </style>
</head>
<body>
    <div class="ui-container" style="width: {width}px; height: {height}px;">
{html_elements}
    </div>
</body>
</html>"""

def generate_html_elements(elements, width, height):
    """Generate HTML for each element"""
    html_lines = []
    
    for element in elements:
        pos = element['position']
        rel_x = (pos['x'] / width) * 100
        rel_y = (pos['y'] / height) * 100
        rel_w = (pos['width'] / width) * 100
        rel_h = (pos['height'] / height) * 100
        
        style = f"left: {rel_x:.2f}%; top: {rel_y:.2f}%; width: {rel_w:.2f}%; height: {rel_h:.2f}%;"
        html_line = generate_single_element(element, style)
        html_lines.append(html_line)
    
    return '\n'.join(html_lines)

def generate_single_element(element, style):
    """Generate HTML for a single element"""
    element_type = element['type']
    text = element.get('text', '')
    
    element_templates = {
        'button': f'<button class="element button" style="{style}">{text or "Button"}</button>',
        'heading': f'<h3 class="element heading" style="{style}">{text or "Heading"}</h3>',
        'text': f'<p class="element text" style="{style}">{text}</p>',
        'input': f'<input class="element input" style="{style}" placeholder="{text or "Enter text..."}">',
        'card': f'<div class="element card" style="{style}">{text}</div>',
        'container': f'<div class="element container" style="{style}"></div>'
    }
    
    return "        " + element_templates.get(element_type, f'<div class="element" style="{style}">{text}</div>')

def generate_css_styles():
    """Generate CSS styles for the UI"""
    return """
        .ui-container {
            position: relative;
            border: 1px solid #ddd;
            margin: 0 auto;
            font-family: Arial, sans-serif;
            background: white;
        }
        .element {
            position: absolute;
            box-sizing: border-box;
        }
        .button {
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            cursor: pointer;
            text-align: center;
            font-size: 14px;
        }
        .heading {
            font-size: 18px;
            font-weight: bold;
            margin: 0;
            color: #333;
        }
        .text {
            font-size: 14px;
            margin: 0;
            padding: 4px;
            color: #666;
        }
        .input {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 8px 12px;
            background: white;
            font-size: 14px;
        }
        .card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 12px;
        }
        .container {
            background: rgba(0, 123, 255, 0.1);
            border: 1px dashed #007bff;
        }"""

def generate_fallback_html():
    """Generate fallback HTML when no elements are detected"""
    return """<div class="container">
    <h1>UI Conversion Result</h1>
    <p>No UI elements were detected in the image.</p>
    <p>Try using a clearer screenshot with distinct UI components.</p>
</div>"""