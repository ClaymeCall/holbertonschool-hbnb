document.addEventListener('DOMContentLoaded', () => {
  //login form
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      await loginUser(email, password);
    });
  }

  //price filter to Index
  const priceFilter = document.getElementById("price-Filter");
  if (priceFilter) {
    populatePriceFilter(priceFilter);
  }

  //places list to Index
  const placesList = document.getElementById("places-list");
  if (placesList) {
    populatePlacesList(placesList);
  }
});

//login function
async function loginUser(email, password) {
  const response = await fetch('http://localhost:5001/api/v1/auth/login', {
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

//price filter function
function populatePriceFilter(priceFilter) {
  const prices = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000];

  prices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = `${price}€`;
    priceFilter.appendChild(option);
  });
}

//place list function
function populatePlacesList(placesList) {
  const places = [
    { name: "Capri Oceanview TinyHouse", price: 200 },
    { name: "New-York CentralPark RoofTopLoft", price: 1550 },
    { name: "Montcuq-en-Couseran Bubble Tent Pyrennees view", price: 60 }
  ];

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `<h3>${place.name}</h3>
    <p>Price per night: ${place.price}€</p>
    <button class="details-button">View Details</button>`;
    placesList.appendChild(card);
  });
}
