// frontend/script.js

async function shortenUrl() {
    const longUrl = document.getElementById("longUrlInput").value;
    const customAlias = document.getElementById("customAliasInput").value;

    const response = await fetch("http://localhost:8000/shorten/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            long_url: longUrl,
            custom_alias: customAlias
        })
    });

    const data = await response.json();
    const shortUrl = data.short_url;

    document.getElementById("shortUrl").innerText = shortUrl;
}
