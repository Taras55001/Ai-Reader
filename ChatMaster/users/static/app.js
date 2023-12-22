function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block';
}

// Функція, яка закриває модальне вікно
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

// Функція для видалення аккаунту
function deleteAccount() {
    // Тут додається логіка для видалення аккаунту
    // Наприклад, ви можете зробити запит на сервер для видалення аккаунту
    // І після успішного видалення аккаунту відобразити сповіщення або перенаправити користувача
    alert('Аккаунт видалено!');
    closeModal('deleteModal');
}

// Додаємо обробники подій для кнопок
document.getElementById('deleteAccountBtn').addEventListener('click', () => {
    openModal('deleteModal');
});

document.getElementById('editProfileBtn').addEventListener('click', () => {
    openModal('editProfileModal');
});