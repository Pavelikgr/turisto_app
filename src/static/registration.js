document.getElementById('registration-form').onsubmit = async (event) => {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const role_id = document.getElementById('role_id').value;

  const userData = {
    username: username,
    email: email,
    password: password,
    role_id: role_id,
  };

  try {
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.log('Ответ сервера при ошибке:', errorData);
      
      if (errorData && errorData.detail === 'REGISTER_USER_ALREADY_EXISTS') {
        const messageError = document.createElement('p');
        messageError.textContent = 'Пользователь с таким логином или email уже существует';
        messageError.classList.add('error-message');
        document.getElementById('registration-form').appendChild(messageError);
      } else {
        console.log('Ошибка регистрации:', errorData.detail);
      }
    } else {
      // Регистрация прошла успешно
      const successMessage = document.createElement('p');
      successMessage.textContent = 'Регистрация прошла успешно!';
      successMessage.classList.add('success-message');
      document.getElementById('registration-form').appendChild(successMessage);

      await delay(5000); // Задержка 5 секунд
      window.location.href = '/'; // Замените 'success.html' на свой путь к странице успешной регистрации
    }
  } catch (error) {
    console.error('Ошибка при выполнении запроса:', error);
  }
};

// Функция задержки
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
