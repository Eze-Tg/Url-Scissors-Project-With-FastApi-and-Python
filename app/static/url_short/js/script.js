// frontend/script.js

document.addEventListener('DOMContentLoaded', function () {
    const urlInput = document.getElementById('longUrlInput');
    const shortUrlDisplay = document.getElementById('shortUrl');
    const qrCodeContainer = document.getElementById('qrCodeContainer');
    const shortUrlContainer = document.getElementById('shortUrlInput');

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
            // const new_short_url = data.url
            // Display short URL
            shortUrlDisplay.textContent = `Shortened URL: ${data.url}`;

        })
        .catch(error => console.error('Error:', error));
    }

    function QrUrl() {
        // Try to QR code the short URL
    const shortUrl = shortUrlDisplay.textContent; // Get the shortened URL from the display

    fetch('/url_to_qr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ target_url: shortUrl }) 
    })
    .then(response => response.blob()) // Convert response to Blob object
    .then(blob => {
        // Create object URL for the Blob
        const imageUrl = URL.createObjectURL(blob);

        // Display QR code
        qrCodeContainer.innerHTML = `<img src="${imageUrl}" alt="QR Code">`;

        // Optionally, you can revoke the object URL to free up resources
        // URL.revokeObjectURL(imageUrl);
    })
    .catch(error => console.error('Error:', error));}

    // Attach click event listener to the button
    const shortenUrlButton = document.getElementById('shortenButton');
    shortenUrlButton.addEventListener('click', shortenUrl);

    const QrcodeButton = document.getElementById('qrcodeButton');
    QrcodeButton.addEventListener('click', QrUrl);
});

