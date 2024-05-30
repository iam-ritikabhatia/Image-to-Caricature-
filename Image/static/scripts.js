document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready');
});

function uploadImage() {
    const input = document.getElementById('imageInput');
    const resultContainer = document.getElementById('result');
    const caricatureImage = document.getElementById('caricatureImage');
    const loadingText = document.getElementById('loadingText');
    const errorMessage = document.getElementById('errorMessage');

    resultContainer.style.display = 'none';
    errorMessage.innerText = '';

    if (input.files && input.files[0]) {
        const formData = new FormData();
        formData.append('image', input.files[0]);

        loadingText.style.display = 'block';

        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                caricatureImage.src = data.caricatureUrl;
                resultContainer.style.display = 'block';
            } else {
                errorMessage.innerText = 'Failed to generate caricature.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.innerText = 'Error occurred while uploading image.';
        })
        .finally(() => {
            loadingText.style.display = 'none';
        });
    }
}
