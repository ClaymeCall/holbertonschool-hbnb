document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      await loginUser(email, password);
    });
  }
});

async function loginUser(email, password) {
  const response = await fetch('https://localhost:5001/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
  });
  // Handle the response
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.token}; path=/`;
    window.location.href = '/index'; /* Flask route for index.html */
  } else {
    alert('Login failed: ' + response.statusText);
  }
}
