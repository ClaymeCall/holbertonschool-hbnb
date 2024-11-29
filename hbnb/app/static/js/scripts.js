document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        await loginUser(email, password);
      } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
      }
    });
  }
});

async function loginUser(email, password) {
  try {
    const response = await fetch('https://localhost:5001/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.token}; path=/`;
      window.location.href = '/index'; /* Flask route for index.html */
    } else {
      const errorData = await response.json();
      alert('Login failed: ' + errorData.message || response.statusText);
    }
  } catch (error) {
    console.error('Network error:', error);
    alert('A network error occurred. Please check your connection and try again.');
  }
}

