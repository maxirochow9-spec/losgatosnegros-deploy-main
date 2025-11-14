// DOM Elements
const accountLink = document.getElementById('accountLink');
const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
const customToast = new bootstrap.Toast(document.getElementById('customToast'));
const toastMessage = document.getElementById('toastMessage');

// Cargar carrito del localStorage
let cart = JSON.parse(localStorage.getItem('cart')) || [];
const cartCount = document.getElementById('cartCount');

// Inicializar la página
function init() {
    updateCartCount();
    setupEventListeners();
    animateOnScroll();
}

// Actualizar contador del carrito
function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    cartCount.textContent = count;
}

// Event listeners
function setupEventListeners() {
    // Account link
    accountLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginModal.show();
    });
    
    // Login/Registration toggles
    document.getElementById('showRegister').addEventListener('click', () => {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('registerForm').style.display = 'block';
    });
    
    document.getElementById('showLogin').addEventListener('click', () => {
        document.getElementById('registerForm').style.display = 'none';
        document.getElementById('loginForm').style.display = 'block';
    });
    
    // Login button
    document.getElementById('loginBtn').addEventListener('click', () => {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        if (email && password) {
            localStorage.setItem('user', JSON.stringify({ email }));
            toastMessage.textContent = 'Inicio de sesión exitoso';
            customToast.show();
            loginModal.hide();
        }
    });
    
    // Register button
    document.getElementById('registerBtn').addEventListener('click', () => {
        const name = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const phone = document.getElementById('registerPhone').value;
        
        if (name && email && password && phone) {
            localStorage.setItem('user', JSON.stringify({ name, email, phone }));
            toastMessage.textContent = 'Registro exitoso. ¡Bienvenido!';
            customToast.show();
            loginModal.hide();
        }
    });
}

// Animaciones al hacer scroll
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.feature-card, .category-card, .stat-card').forEach(el => {
        observer.observe(el);
    });
}

// Smooth scroll para anclas
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Inicializar cuando cargue el DOM
document.addEventListener('DOMContentLoaded', init);
