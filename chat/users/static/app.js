function editProfile() {
    const editModal = document.getElementById('editProfileModal');
    editModal.style.display = 'block';
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function saveChanges() {
    const newUsername = document.getElementById('username').value;
    const newEmail = document.getElementById('email').value;

    const data = JSON.stringify({ username: newUsername, email: newEmail });

    fetch('/users/change', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Додаємо CSRF-токен у заголовок
        },
        body: data,
    })
    .then(response => {
        if (response.ok) {
            alert('Зміни збережено!');
            closeModal('editProfileModal');
        } else {
            throw new Error('Помилка при збереженні змін!');
        }
    })
    .catch(error => {
        alert(error.message);
    });
}

// Функція, яка закриває модальне вікно
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

function confirmDelete() {
    const confirmModal = document.getElementById('confirmDeleteModal');
    confirmModal.style.display = 'block';
}

// Функція для видалення облікового запису
function deleteAccount() {
    // Отримання CSRF токену
    const csrftoken = getCookie('csrftoken');
    
    fetch('/users/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Обліковий запис успішно видалено!');
            // Якщо потрібно перенаправити після видалення, використовуйте window.location = '/новий_шлях';
        } else {
            throw new Error('Помилка при видаленні облікового запису!');
        }
    })
    .catch(error => {
        alert(error.message);
    });
}

// Функція для підтвердження видалення
function deleteConfirmation() {
    deleteAccount(); // Виклик функції видалення
    closeModal('confirmDeleteModal'); // Закриття підтвердження
}