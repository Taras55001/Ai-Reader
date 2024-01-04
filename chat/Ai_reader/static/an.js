function sendMessage() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);

    fetch('/your_url_here/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Отримано відповідь:', data);
        // Тут ви можете обробити отримані дані
    })
    .catch(error => {
        console.error('Помилка:', error);
    });
}