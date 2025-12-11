// Sample products data with realistic images
const products = [
    {
        id: 1,
        name: "Whisky Escocés 12 Años",
        price: 15990,
        image: "https://desaonline.vtexassets.com/arquivos/ids/157202-800-auto?v=637437364118770000&width=800&height=auto&aspect=true",
        type: "alcoholic"
    },
    {
        id: 2,
        name: "Vino Tinto Reserva",
        price: 8990,
        image: "https://media.falabella.com/tottusCL/02000039_1/w=800,h=800,fit=pad",
        type: "alcoholic"
    },
    {
        id: 3,
        name: "Cerveza Artesanal IPA",
        price: 2490,
        image: "https://unimarc.vtexassets.com/arquivos/ids/232413/000000000000663374-UN-01.jpg?v=638167546055270000",
        type: "alcoholic"
    },
    {
        id: 4,
        name: "Jugo de Naranja Natural",
        price: 1990,
        image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQd67gBvzoCeNMdd6VAaXJXZAt3anupxeUfBA&s",
        type: "non-alcoholic"
    },
    {
        id: 5,
        name: "Agua Mineral con Gas",
        price: 1290,
        image: "https://tost.cl/cdn/shop/files/Disenosintitulo-2024-04-02T164739.838_1200x.png?v=1738742454",
        type: "non-alcoholic"
    },
    {
        id: 6,
        name: "Gaseosa CoCa Cola",
        price: 1490,
        image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXO9xZmjHdxttGK0ga-kIal4qwE67dEYAE3Q&s",
        type: "non-alcoholic"
    },
    {
        id: 7,
        name: "Ron Dorado Añejo",
        price: 12990,
        image: "https://cdnx.jumpseller.com/comercial-jp/image/51061622/ron_dorado_mitjans_750cc_y_1000cc.jfif?1722550406",
        type: "alcoholic"
    },
    {
        id: 8,
        name: "Té Helado de Durazno",
        price: 2190,
        image: "https://santaisabel.vtexassets.com/arquivos/ids/426763/Ice-Tea-Lipton-Durazno-15-L.jpg?v=638602811286100000",
        type: "non-alcoholic"
    }
];

// DOM Elements
const productsContainer = document.getElementById('productsContainer');
const searchInput = document.getElementById('searchInput');
const typeFilter = document.getElementById('typeFilter');
const cartLink = document.getElementById('cartLink');
const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));
const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
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
    renderProducts();
    updateCartCount();
    setupEventListeners();
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
        productCard.className = 'col-md-6 col-lg-4 col-xl-3 mb-4';
        productCard.innerHTML = `
            <div class="product-card">
                <img src="${product.image}" class="product-img" alt="${product.name}">
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
    
    // Mostrar modal de producto eliminado
    showProductRemovedModal();
}

// Mostrar modal de producto eliminado
function showProductRemovedModal() {
    const modal = document.getElementById('productRemovedModal');
    if (modal) {
        modal.style.display = 'flex';
        
        const closeBtn = document.getElementById('productRemovedBtn');
        if (closeBtn) {
            closeBtn.onclick = function() {
                modal.style.display = 'none';
            };
        }
        
        // Cerrar automáticamente después de 3 segundos
        setTimeout(function() {
            modal.style.display = 'none';
        }, 3000);
    }
}

// Clear cart
function clearCart() {
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
    showCartClearedModal();
}

// Mostrar modal de carrito vaciado
function showCartClearedModal() {
    const modal = document.getElementById('cartClearedModal');
    if (modal) {
        modal.style.display = 'flex';
        
        const closeBtn = document.getElementById('cartClearedBtn');
        if (closeBtn) {
            closeBtn.onclick = function() {
                modal.style.display = 'none';
            };
        }
        
        setTimeout(function() {
            modal.style.display = 'none';
        }, 3000);
    }
}

// Mostrar modal de confirmar vaciar carrito
function showClearCartConfirmModal() {
    return new Promise((resolve) => {
        const modal = document.getElementById('clearCartConfirmModal');
        if (modal) {
            modal.style.display = 'flex';
            
            const confirmBtn = document.getElementById('clearCartConfirmBtn');
            const cancelBtn = document.getElementById('clearCartCancelBtn');
            
            confirmBtn.onclick = function() {
                modal.style.display = 'none';
                resolve(true);
            };
            
            cancelBtn.onclick = function() {
                modal.style.display = 'none';
                resolve(false);
            };
        } else {
            resolve(confirm('¿Estás seguro de que deseas vaciar el carrito?'));
        }
    });
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
        cartModal.hide();
        checkoutModal.show();
    });
    
    // Clear cart button
    clearCartBtn.addEventListener('click', async () => {
        if (cart.length === 0) return;
        const confirmed = await showClearCartConfirmModal();
        if (confirmed) {
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
        
        // Generate WhatsApp message
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
        
        toastMessage.textContent = 'Pedido enviado! Redirigiendo a WhatsApp...';
        customToast.show();
        
        setTimeout(() => {
            window.open(whatsappUrl, '_blank');
        }, 1500);
    });
    
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
            toastMessage.textContent = 'Registro exitoso. Bienvenido!';
            customToast.show();
            loginModal.hide();
        }
    });
    
    // Filter inputs
    searchInput.addEventListener('input', filterProducts);
    typeFilter.addEventListener('change', filterProducts);
}

// Initialize the app
document.addEventListener('DOMContentLoaded', init);