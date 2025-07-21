async function detectRoast() {
    const input = document.getElementById('imageInput');
    const resultDiv = document.getElementById('result');
    const preview = document.getElementById('preview');
    
    if (!input.files[0]) {
        resultDiv.innerText = 'Please select an image.';
        return;
    }

    const formData = new FormData();
    formData.append('file', input.files[0]);

    // Display image preview
    preview.src = URL.createObjectURL(input.files[0]);
    preview.style.display = 'block';

    try {
        const response = await fetch('https://<your-azure-app-name>.azurewebsites.net/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        resultDiv.innerText = `Roast Level: ${data.roast_level} (Confidence: ${data.confidence})`;
    } catch (error) {
        resultDiv.innerText = 'Error: Could not connect to the server.';
        console.error(error);
    }
}