
// DOM Elements
const productsContainer = document.getElementById('productsContainer');
const searchInput = document.getElementById('searchInput');
const typeFilter = document.getElementById('typeFilter');
const cartLink = document.getElementById('cartLink');
const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));
const loginModalEl = document.getElementById('loginModal');
const loginModal = loginModalEl ? new bootstrap.Modal(loginModalEl) : null;
const accountLink = document.getElementById('accountLink');
const cartCount = document.getElementById('cartCount');
const cartItems = document.getElementById('cartItems');
const totalAmount = document.getElementById('totalAmount');
const clearCartBtn = document.getElementById('clearCart');
const checkoutBtn = document.getElementById('checkoutBtn');
const sendOrderBtn = document.getElementById('sendOrder');
const customToast = new bootstrap.Toast(document.getElementById('customToast'));
const toastMessage = document.getElementById('toastMessage');

// Cart array
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Initialize the page
function init() {
    // Si el servidor ya renderizó productos en el DOM, construir el array desde el DOM
    if (productsContainer && productsContainer.children.length > 0) {
        const domProducts = buildProductsFromDOM();
        if (domProducts.length > 0) {
            products = domProducts;
            // No re-render para mantener el HTML que Django ya colocó,
            // pero enlazamos los botones existentes a las funciones.
            bindAddButtons();
        } else {
            renderProducts();
        }
    } else {
        renderProducts();
    }
    updateCartCount();
    setupEventListeners();
    applyQueryFilters();
}

// Construye un arreglo de productos a partir del HTML renderizado por el servidor
function buildProductsFromDOM() {
    const items = [];
    const nodes = document.querySelectorAll('#productsContainer .product-card');
    nodes.forEach(node => {
        try {
            const idBtn = node.querySelector('.btn-add');
            const id = idBtn ? parseInt(idBtn.getAttribute('data-id')) : null;
            const nameEl = node.querySelector('.product-title');
            const priceEl = node.querySelector('.product-price');
            const imgEl = node.querySelector('img');
            const badge = node.querySelector('.badge');

            let price = 0;
            if (priceEl) {
                // Extraer números del texto como $12.990
                const num = priceEl.textContent.replace(/[^0-9]/g, '');
                price = num ? parseInt(num, 10) : 0;
            }

            let type = '';
            if (badge) {
                const txt = badge.textContent.toLowerCase();
                if (txt.includes('alcoh')) type = 'alcoholic';
                else if (txt.includes('sin') || txt.includes('no')) type = 'non-alcoholic';
            }

            items.push({
                id: id || Math.floor(Math.random() * 1000000),
                name: nameEl ? nameEl.textContent.trim() : 'Producto',
                price: price,
                image: imgEl ? imgEl.getAttribute('src') : '',
                type: type
            });
        } catch (e) {
            // Ignorar elementos mal formados
        }
    });
    return items;
}

// Enlaza los botones "Agregar" que ya existen en el DOM
function bindAddButtons() {
    document.querySelectorAll('.btn-add').forEach(button => {
        button.removeEventListener('click', addButtonHandler);
        button.addEventListener('click', addButtonHandler);
    });
}

function addButtonHandler(e) {
    const productId = parseInt(e.currentTarget.getAttribute('data-id'));
    addToCart(productId);
}

// Apply filters from URL query string
function applyQueryFilters() {
    const urlParams = new URLSearchParams(window.location.search);
    const typeParam = urlParams.get('type');
    
    if (typeParam) {
        typeFilter.value = typeParam;
        filterProducts();
    }
}

// Render products
function renderProducts(filteredProducts = products) {
    productsContainer.innerHTML = '';
    
    if (filteredProducts.length === 0) {
        productsContainer.innerHTML = '<div class="col-12"><p class="text-center text-muted">No se encontraron productos</p></div>';
        return;
    }
    
    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'col-md-6 col-lg-4 col-xl-3 mb-4 product-item';
        productCard.innerHTML = `
            <div class="product-card">
                <img src="${product.image}" class="product-img" alt="${product.name}" loading="lazy">
                <div class="product-body">
                    <h5 class="product-title">${product.name}</h5>
                    <p class="product-price">$${product.price.toLocaleString('es-CL')}</p>
                    <button class="btn btn-add" data-id="${product.id}">
                        <i class="bi bi-cart-plus"></i> Agregar al carrito
                    </button>
                </div>
            </div>
        `;
        productsContainer.appendChild(productCard);
    });
    
    // Add event listeners to add buttons
    document.querySelectorAll('.btn-add').forEach(button => {
        button.addEventListener('click', () => {
            const productId = parseInt(button.getAttribute('data-id'));
            addToCart(productId);
        });
    });
}

// Add to cart function
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Show toast notification
    toastMessage.textContent = `${product.name} agregado al carrito`;
    customToast.show();
}

// Update cart count
function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    cartCount.textContent = count;
}

// Render cart items
function renderCart() {
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="text-center text-muted">Tu carrito está vacío</p>';
        totalAmount.textContent = '$0';
        return;
    }
    
    let cartHTML = '';
    let total = 0;
    
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        cartHTML += `
            <div class="cart-item">
                <div class="d-flex align-items-center">
                    <img src="${item.image}" class="cart-img" alt="${item.name}">
                    <div class="ms-3 flex-grow-1">
                        <h6 class="cart-title">${item.name}</h6>
                        <p class="mb-0 text-muted">$${item.price.toLocaleString('es-CL')}</p>
                    </div>
                    <div class="quantity-control">
                        <button class="quantity-btn minus" data-id="${item.id}">-</button>
                        <input type="number" class="quantity-input" value="${item.quantity}" min="1" data-id="${item.id}">
                        <button class="quantity-btn plus" data-id="${item.id}">+</button>
                    </div>
                    <div class="ms-3">
                        <p class="mb-0">$${itemTotal.toLocaleString('es-CL')}</p>
                        <button class="btn btn-sm btn-outline-danger mt-2 remove-item" data-id="${item.id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    cartItems.innerHTML = cartHTML;
    totalAmount.textContent = `$${total.toLocaleString('es-CL')}`;
    
    // Add event listeners to quantity controls
    document.querySelectorAll('.quantity-btn.minus').forEach(button => {
        button.addEventListener('click', () => {
            const id = parseInt(button.getAttribute('data-id'));
            updateQuantity(id, -1);
        });
    });
    
    document.querySelectorAll('.quantity-btn.plus').forEach(button => {
        button.addEventListener('click', () => {
            const id = parseInt(button.getAttribute('data-id'));
            updateQuantity(id, 1);
        });
    });
    
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', () => {
            const id = parseInt(input.getAttribute('data-id'));
            const newQuantity = parseInt(input.value);
            if (newQuantity > 0) {
                const currentItem = cart.find(item => item.id === id);
                if (currentItem) {
                    updateQuantity(id, newQuantity - currentItem.quantity);
                }
            } else {
                input.value = 1;
            }
        });
    });
    
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', () => {
            const id = parseInt(button.getAttribute('data-id'));
            removeFromCart(id);
        });
    });
}

// Update item quantity
function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(id);
        return;
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

// Remove item from cart
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

// Clear cart
function clearCart() {
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

// Filter products
function filterProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    const type = typeFilter.value;
    
    let filtered = products;
    
    if (searchTerm) {
        filtered = filtered.filter(product => 
            product.name.toLowerCase().includes(searchTerm)
        );
    }
    
    if (type) {
        filtered = filtered.filter(product => product.type === type);
    }
    
    renderProducts(filtered);
}

// Setup event listeners
function setupEventListeners() {
    // Cart link
    cartLink.addEventListener('click', (e) => {
        e.preventDefault();
        renderCart();
        cartModal.show();
    });
    
    // Checkout button
    checkoutBtn.addEventListener('click', () => {
        if (cart.length === 0) {
            toastMessage.textContent = 'Tu carrito está vacío';
            customToast.show();
            return;
        }

        // Requerir que el usuario esté autenticado (variable `IS_AUTH` definida en template)
        if (typeof IS_AUTH !== 'undefined' && !IS_AUTH) {
            // Redirigir a la página de login con next para volver a catálogo
            const next = encodeURIComponent(window.location.pathname + window.location.search);
            window.location.href = '/login/?next=' + next;
            return;
        }

        cartModal.hide();
        checkoutModal.show();
    });
    
    // Clear cart button
    clearCartBtn.addEventListener('click', () => {
        if (cart.length === 0) return;
        if (confirm('¿Estás seguro de que deseas vaciar el carrito?')) {
            clearCart();
        }
    });
    
    // Send order button
    sendOrderBtn.addEventListener('click', () => {
        const name = document.getElementById('customerName').value;
        const address = document.getElementById('customerAddress').value;
        const phone = document.getElementById('customerPhone').value;
        
        if (!name || !address || !phone) {
            toastMessage.textContent = 'Por favor completa todos los campos';
            customToast.show();
            return;
        }
        
        // Enviar pedido al servidor para persistir
        const payload = {
            items: cart.map(i => ({ id: i.id, quantity: i.quantity })),
            direccion: address,
            telefono: phone
        };

        // Obtener csrf token desde cookie
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

        const csrftoken = getCookie('csrftoken');

        fetch('/orders/create/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken || ''
            },
            body: JSON.stringify(payload)
        }).then(r => r.json()).then(data => {
            if (data && data.success) {
                // Opcional: enviar a WhatsApp también
                let message = `¡Hola! Quisiera hacer un pedido:\n\n`;
                cart.forEach(item => {
                    message += `- ${item.name} x${item.quantity} = $${(item.price * item.quantity).toLocaleString('es-CL')}\n`;
                });
                message += `\nTotal: $${cart.reduce((total, item) => total + (item.price * item.quantity), 0).toLocaleString('es-CL')}\n\n`;
                message += `Nombre: ${name}\n`;
                message += `Dirección: ${address}\n`;
                message += `Teléfono: ${phone}`;

                const encodedMessage = encodeURIComponent(message);
                const whatsappUrl = `https://wa.me/56966344411?text=${encodedMessage}`;

                clearCart();
                checkoutModal.hide();
                toastMessage.textContent = 'Pedido guardado y enviado! Redirigiendo a WhatsApp...';
                customToast.show();

                setTimeout(() => {
                    window.open(whatsappUrl, '_blank');
                }, 1500);
            } else {
                const err = (data && data.error) ? data.error : 'Error al crear pedido';
                toastMessage.textContent = err;
                customToast.show();
            }
        }).catch(err => {
            toastMessage.textContent = 'Error al conectar con el servidor';
            customToast.show();
            console.error(err);
        });
    });
    
    // Account link: sólo añadir handler si el enlace es el antiguo '#'
    if (accountLink) {
        const href = accountLink.getAttribute('href');
        if (href === '#' && loginModal) {
            accountLink.addEventListener('click', (e) => {
                e.preventDefault();
                loginModal.show();
            });
        }
    }
    
    // Login/Registration toggles
    // Login/Registration modal buttons should redirect to server-side pages
    const showRegisterBtn = document.getElementById('showRegister');
    const showLoginBtn = document.getElementById('showLogin');
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');

    function redirectToLogin() {
        const next = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = '/login/?next=' + next;
    }

    function redirectToRegister() {
        const next = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = '/register/?next=' + next;
    }

    if (showRegisterBtn) showRegisterBtn.addEventListener('click', (e) => { e.preventDefault(); redirectToRegister(); });
    if (showLoginBtn) showLoginBtn.addEventListener('click', (e) => { e.preventDefault(); redirectToLogin(); });
    if (loginBtn) loginBtn.addEventListener('click', (e) => { e.preventDefault(); redirectToLogin(); });
    if (registerBtn) registerBtn.addEventListener('click', (e) => { e.preventDefault(); redirectToRegister(); });
    
    // Filter inputs
    searchInput.addEventListener('input', filterProducts);
    typeFilter.addEventListener('change', filterProducts);
}

// Initialize the app
document.addEventListener('DOMContentLoaded', init);
