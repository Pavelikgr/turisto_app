document.addEventListener('DOMContentLoaded', function() {
  // Находим форму логина
  const loginForm = document.getElementById('login-form');

  // Добавляем обработчик события отправки формы
  loginForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем отправку формы по умолчанию

    // Получаем значения полей формы
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Создаем объект FormData и добавляем значения полей формы
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    // Отправляем запрос на сервер для аутентификации
    fetch('/auth/login', {
      method: 'POST',
      body: formData
    })
    .then(function(response) {
      if (response.ok) {
        // Отображаем сообщение об успешном входе
        const successMessage = document.createElement('p');
        successMessage.textContent = 'Вы успешно вошли!';
        successMessage.classList.add('success-message');
        document.getElementById('login-form').appendChild(successMessage);
    
        // Задержка 5 секунд перед перенаправлением на главную страницу
        setTimeout(function() {
          window.location.href = '/profile/ ';
        }, 5000);
      } else if (response.status === 400) {
        // Если получена ошибка 400 Bad Request
        response.json().then(function(data) {
          if (data.detail === 'LOGIN_BAD_CREDENTIALS') {
            // Если детализация ошибки "LOGIN_BAD_CREDENTIALS"
            // Отображаем сообщение об ошибке на странице
            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'Неверный логин или пароль';
            errorMessage.classList.add('error-message');
            document.getElementById('login-form').appendChild(errorMessage);
          }
        });
      } else {
        // Если получена другая ошибка, обрабатываем её соответствующим образом
        console.log('Ошибка:', response.status);
      }
    })
  });
});