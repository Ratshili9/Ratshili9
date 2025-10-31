function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select an image file');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        
        if (data.success) {
            document.getElementById('htmlOutput').textContent = data.html;
            document.getElementById('preview').innerHTML = data.html;
            document.getElementById('result').style.display = 'block';
        } else {
            showError('Error: ' + data.error);
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        showError('Network error: ' + error);
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Preview image when selected
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('result').style.display = 'none';
        document.getElementById('error').style.display = 'none';
    }
});