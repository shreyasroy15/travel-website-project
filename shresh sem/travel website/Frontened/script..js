// API Base URL
const API_BASE_URL = 'http://localhost:5000';

// User Authentication Functions
async function registerUser(username, password, email) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, email })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }
        return data;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

async function loginUser(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify({
            id: data.user_id,
            username: data.username
        }));
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Destination Functions
async function getDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error('Failed to fetch destinations');
        }
        return data;
    } catch (error) {
        console.error('Error fetching destinations:', error);
        throw error;
    }
}

// Hotel Functions
async function getHotels() {
    try {
        const response = await fetch(`${API_BASE_URL}/hotels`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error('Failed to fetch hotels');
        }
        return data;
    } catch (error) {
        console.error('Error fetching hotels:', error);
        throw error;
    }
}

// Booking Functions
async function createBooking(bookingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Booking failed');
        }
        return data;
    } catch (error) {
        console.error('Booking error:', error);
        throw error;
    }
}

async function getUserBookings(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings/${userId}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error('Failed to fetch bookings');
        }
        return data;
    } catch (error) {
        console.error('Error fetching bookings:', error);
        throw error;
    }
}

// Utility Functions
function checkAuthStatus() {
    const user = localStorage.getItem('user');
    if (!user) {
        window.location.href = 'login.html';
        return null;
    }
    return JSON.parse(user);
}

function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// DOM Event Handlers
document.addEventListener('DOMContentLoaded', () => {
    // Login Form Handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                await loginUser(username, password);
                window.location.href = 'index.html';
            } catch (error) {
                alert(error.message);
            }
        });
    }

    // Register Form Handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            const email = document.getElementById('regEmail').value;

            try {
                await registerUser(username, password, email);
                alert('Registration successful! Please login.');
                window.location.href = 'login.html';
            } catch (error) {
                alert(error.message);
            }
        });
    }

    // Load Destinations
    const destinationsContainer = document.getElementById('destinationsContainer');
    if (destinationsContainer) {
        loadDestinations();
    }

    // Load Hotels
    const hotelsContainer = document.getElementById('hotelsContainer');
    if (hotelsContainer) {
        loadHotels();
    }
});

// Content Loading Functions
async function loadDestinations() {
    try {
        const destinations = await getDestinations();
        const container = document.getElementById('destinationsContainer');
        if (container) {
            container.innerHTML = destinations.map(dest => `
                <div class="destination-card">
                    <img src="${dest.image_url}" alt="${dest.name}">
                    <h3>${dest.name}</h3>
                    <p>${dest.description}</p>
                    <p class="price">$${dest.price}</p>
                    <button onclick="bookDestination(${dest.id})">Book Now</button>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

async function loadHotels() {
    try {
        const hotels = await getHotels();
        const container = document.getElementById('hotelsContainer');
        if (container) {
            container.innerHTML = hotels.map(hotel => `
                <div class="hotel-card">
                    <img src="${hotel.image_url}" alt="${hotel.name}">
                    <h3>${hotel.name}</h3>
                    <p>${hotel.description}</p>
                    <p>Location: ${hotel.location}</p>
                    <p class="price">$${hotel.price_per_night} per night</p>
                    <button onclick="bookHotel(${hotel.id})">Book Now</button>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading hotels:', error);
    }
}
