// frontend/script.js

document.addEventListener('DOMContentLoaded', function () {
    const urlInput = document.getElementById('longUrlInput');
    const shortUrlDisplay = document.getElementById('shortUrl');
    const qrCodeContainer = document.getElementById('qrCodeContainer');

    function shortenUrl() {
        const longUrl = urlInput.value.trim();

        fetch('/url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ target_url: longUrl })
        })
        .then(response => response.json())
        .then(data => {
            // Display short URL
            shortUrlDisplay.textContent = `Shortened URL: ${data.url}`;

            // Display QR code
            qrCodeContainer.innerHTML = `<img src="data:image/png;base64,${data.qr_code}" alt="QR Code">`;
        })
        .catch(error => console.error('Error:', error));
    }

    // Attach click event listener to the button
    const shortenUrlButton = document.getElementById('shortenButton');
    shortenUrlButton.addEventListener('click', shortenUrl);
});

