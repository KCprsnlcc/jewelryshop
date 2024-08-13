// shop/static/shop/scripts.js

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  const searchButton = document.getElementById("search-button");
  const categoryCheckboxes = document.querySelectorAll(
    'input[name="categories"]'
  );
  const productList = document.getElementById("product-list");
  const loader = document.getElementById("loader");

  function showLoader() {
    loader.style.display = "block";
  }

  function hideLoader() {
    loader.style.display = "none";
  }

  function filterProducts() {
    showLoader();
    const searchQuery = searchInput.value.toLowerCase();
    const selectedCategories = Array.from(categoryCheckboxes)
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value);

    const products = document.querySelectorAll(".product");

    products.forEach((product) => {
      const productName = product.getAttribute("data-name").toLowerCase();
      const productCategory = product.getAttribute("data-category");

      const matchesSearch = productName.includes(searchQuery);
      const matchesCategory =
        selectedCategories.length === 0 ||
        selectedCategories.includes(productCategory);

      if (matchesSearch && matchesCategory) {
        product.style.display = "block";
      } else {
        product.style.display = "none";
      }
    });

    setTimeout(hideLoader, 500); // Simulate loading delay
  }

  searchButton.addEventListener("click", filterProducts);
  searchInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      filterProducts();
    }
  });

  categoryCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", filterProducts);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const addToCartButton = document.getElementById("add-to-cart-button");
  const addToCartModal = document.getElementById("add-to-cart-modal");
  const closeAddToCart = document.getElementById("close-add-to-cart");
  const confirmAddToCart = document.getElementById("confirm-add-to-cart");
  const cartModal = document.getElementById("cart-modal");
  const closeCart = document.getElementById("close-cart");
  const cartItemsContainer = document.getElementById("cart-items");
  const cartTotalElement = document.getElementById("cart-total");
  const applyVoucherButton = document.getElementById("apply-voucher");
  const discountMessage = document.getElementById("discount-message");
  const checkoutButton = document.getElementById("checkout-button");
  const notification = document.getElementById("notification");
  const cartCountElement = document.getElementById("cart-count");
  const floatingCartButton = document.getElementById("floating-cart-button");
  const paypalModal = document.getElementById("paypal-modal");
  const closePayPal = document.getElementById("close-paypal");
  const confirmPayPal = document.getElementById("confirm-paypal");

  let cart = [];
  let discount = 0;

  function showNotification(message, type = "success") {
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = "block";
    setTimeout(() => {
      notification.style.display = "none";
    }, 3000);
  }

  function openModal(modal) {
    modal.style.display = "block";
  }

  function closeModal(modal) {
    modal.style.display = "none";
  }

  function updateCartTotal() {
    let total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    total = total - total * discount;
    cartTotalElement.textContent = total.toFixed(2);
  }

  function updateCartCount() {
    cartCountElement.textContent = cart.reduce(
      (sum, item) => sum + item.quantity,
      0
    );
  }

  function renderCartItems() {
    cartItemsContainer.innerHTML = "";
    cart.forEach((item, index) => {
      const cartItem = document.createElement("div");
      cartItem.className = "cart-item";
      cartItem.innerHTML = `
                <p>${item.name}</p>
                <p>PHP ${item.price}</p>
                <input type="number" value="${item.quantity}" min="1" class="cart-quantity" data-index="${index}">
                <button class="remove-cart-item" data-index="${index}">Remove</button>
            `;
      cartItemsContainer.appendChild(cartItem);
    });

    document.querySelectorAll(".cart-quantity").forEach((input) => {
      input.addEventListener("change", function () {
        const index = this.getAttribute("data-index");
        cart[index].quantity = parseInt(this.value);
        updateCartTotal();
        updateCartCount();
      });
    });

    document.querySelectorAll(".remove-cart-item").forEach((button) => {
      button.addEventListener("click", function () {
        const index = this.getAttribute("data-index");
        cart.splice(index, 1);
        renderCartItems();
        updateCartTotal();
        updateCartCount();
      });
    });

    updateCartTotal();
    updateCartCount();
  }

  addToCartButton.addEventListener("click", function () {
    openModal(addToCartModal);
  });

  closeAddToCart.addEventListener("click", function () {
    closeModal(addToCartModal);
  });

  confirmAddToCart.addEventListener("click", function () {
    const productName =
      document.querySelector(".product-detail h3").textContent;
    const productPrice = parseFloat(
      document
        .querySelector(".product-detail .price")
        .textContent.replace("PHP ", "")
    );
    const quantity = parseInt(document.getElementById("cart-quantity").value);
    const existingProductIndex = cart.findIndex(
      (item) => item.name === productName
    );

    if (existingProductIndex > -1) {
      cart[existingProductIndex].quantity += quantity;
    } else {
      cart.push({ name: productName, price: productPrice, quantity: quantity });
    }

    closeModal(addToCartModal);
    renderCartItems();
    showNotification("Item added to cart!", "success");
  });

  floatingCartButton.addEventListener("click", function () {
    openModal(cartModal);
  });

  closeCart.addEventListener("click", function () {
    closeModal(cartModal);
  });

  applyVoucherButton.addEventListener("click", function () {
    const voucherCode = document
      .getElementById("voucher")
      .value.trim()
      .toUpperCase();
    if (voucherCode === "DISCOUNT30") {
      discount = 0.3;
      discountMessage.textContent = "Voucher applied! 30% discount.";
    } else {
      discount = 0;
      discountMessage.textContent = "Invalid voucher code.";
    }
    updateCartTotal();
  });

  checkoutButton.addEventListener("click", function () {
    const location = document.getElementById("location").value;
    const paymentMethod = document.getElementById("payment-method").value;

    if (!location) {
      alert("Please enter your location.");
      return;
    }

    if (cart.length === 0) {
      alert("Your cart is empty.");
      return;
    }

    if (paymentMethod === "paypal") {
      openModal(paypalModal);
    } else {
      showNotification("Order placed successfully!", "success");
      cart = [];
      renderCartItems();
      closeModal(cartModal);
    }
  });

  closePayPal.addEventListener("click", function () {
    closeModal(paypalModal);
    showNotification("Order placed successfully!", "success");
    cart = [];
    renderCartItems();
    closeModal(cartModal);
  });

  confirmPayPal.addEventListener("click", function () {
    closeModal(paypalModal);
    showNotification("Order placed successfully!", "success");
    cart = [];
    renderCartItems();
    closeModal(cartModal);
  });
});
