document.getElementById('big-button').addEventListener('click', async function() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentUrl = tab.url;

    const response = await fetch('http://localhost:8000/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: currentUrl })
    });

    const data = await response.json();
    console.log("Summary from backend:", data.summary);

    // Display the summary (optional)
    document.getElementById('summary').textContent = data.summary;
});
