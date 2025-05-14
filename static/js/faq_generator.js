function checkProgress() {
    fetch('/ans/get_progress/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        timeout: 10000 // 10 seconds
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        return response.json();
    })
    .then(data => {
        document.getElementById('progress-bar').style.width = data.progress + '%';
        document.getElementById('status-message').innerText = data.status_message;
        if (data.progress < 100) {
            setTimeout(checkProgress, 5000); // Poll every 5 seconds
        } else {
            console.log('Processing complete:', data);
        }
    })
    .catch(error => {
        console.error('Error fetching progress:', error);
        setTimeout(checkProgress, 10000); // Retry after 10 seconds
    });
}

document.getElementById('faq-form').addEventListener('submit', function() {
    checkProgress();
});