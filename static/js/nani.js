// Ajax xử lý lọc và sắp xếp không load lại trang
$(document).ready(function(){
    function updateProductList() {
        $.ajax({
            url: $('#filter-form').attr('action'),
            type: $('#filter-form').attr('method'),
            data: $('#filter-form').serialize() + '&' + $('#sort-form').serialize(),
            success: function(response){
                $('#product-list-container').html(response.products_html);
            }
        });
    }

    $('#filter-form').on('submit', function(e){
        e.preventDefault();
        updateProductList();
    });

    $('#sort-form select').on('change', function(){
        updateProductList();
    });

    $(document).on('click', '.page-link', function(e){
        e.preventDefault();
        var page = $(this).data('page');
        $.ajax({
            url: window.location.pathname,
            type: 'get',
            data: $('#filter-form').serialize() + '&' + $('#sort-form').serialize() + '&page=' + page,
            success: function(response){
                $('#product-list-container').html(response.products_html);
            }
        });
    });
});

// Lấy nút
const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// Khi người dùng cuộn xuống 150px từ đầu trang, hiển thị nút
window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
}

// Khi người dùng nhấp vào nút, cuộn lên đầu trang
scrollToTopBtn.addEventListener("click", function() {
    document.body.scrollTop = 0; // Dành cho Safari
    document.documentElement.scrollTop = 0; // Dành cho Chrome, Firefox, IE và Opera
});

// Thêm bớt sản phẩm
document.addEventListener('DOMContentLoaded', function() {
    function setupEventListeners() {
        var updateBtns = document.getElementsByClassName('update-cart');
        var changeQuantityBtns = document.getElementsByClassName('chg-quantity');
        var deleteBtns = document.getElementsByClassName('delete-item');

        // console.log('Setting up event listeners.');

        for (var i = 0; i < updateBtns.length; i++) {
            // console.log('Adding event listener for update button:', updateBtns[i]);
            updateBtns[i].addEventListener('click', handleUpdateCartClick);
        }

        for (var i = 0; i < changeQuantityBtns.length; i++) {
            // console.log('Adding event listener for change quantity button:', changeQuantityBtns[i]);
            changeQuantityBtns[i].addEventListener('click', handleChangeQuantityClick);
        }

        for (var i = 0; i < deleteBtns.length; i++) {
            // console.log('Adding event listener for delete button:', deleteBtns[i]);
            deleteBtns[i].addEventListener('click', handleDeleteItemClick);
        }
    }

    function handleUpdateCartClick(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log('Update cart clicked');
        var productId = this.dataset.product;
        var action = this.dataset.action;
        if (user === "AnonymousUser") {
            console.log('User not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    }

    function handleChangeQuantityClick(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log('Change quantity clicked');
        var productId = this.dataset.product;
        var action = this.dataset.action;
        if (user === "AnonymousUser") {
            console.log('User not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    }

    function handleDeleteItemClick(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log('Delete item clicked');
        var productId = this.dataset.product;
        var action = 'remove_all';  // đảm bảo action là 'remove_all' khi click vào delete-item
        if (user === "AnonymousUser") {
            console.log('User not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    }

    function updateUserOrder(productId, action) {
        console.log('Updating user order:', { productId, action });
        var url = '/orders/update_item/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            console.log('data', data);
            updateCartUI(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function formatCurrency(value) {
        const formatter = new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });
    
        let formattedValue = formatter.format(value);
        formattedValue = formattedValue.replace(/\./g, '#').replace(/,/g, '.').replace(/#/g, ',');
        return formattedValue.replace('₫', '').trim();
    }

    function updateCartUI(data) {
        // console.log('Updating cart UI with data:', data);

        var itemElement = document.querySelector(`.cart-list .product-widget[data-product="${data.productId}"]`);
        if (itemElement) {
            var quantityElement = itemElement.querySelector('.item-quantity');
            if (quantityElement) {
                quantityElement.innerText = data.itemQuantity + 'x';
            }

            var totalElement = itemElement.querySelector('.item-total');
            if (totalElement) {
                totalElement.innerText = formatCurrency(data.itemQuantity * data.productPrice) + ' ₫';
            }

            if (data.itemQuantity <= 0 || data.action === 'remove_all') {  // Đảm bảo xóa mục nếu hành động là 'remove_all'
                itemElement.remove();
            }
        }

        var cartTotalItemsElement = document.querySelector('.header-ctn .cart-total-items');
        if (cartTotalItemsElement) {
            // console.log('Updating total items in cart to:', data.cartTotalItems);
            cartTotalItemsElement.innerText = data.cartTotalItems;
        } else {
            // console.log('Cart total items element not found.');
        }

        var cartTotalMoneyElements = document.querySelectorAll('.total-money');
        cartTotalMoneyElements.forEach(function(element) {
            element.innerText = formatCurrency(data.cartTotalMoney) + ' ₫';
        });

        var cartItemElement = document.querySelector(`.row[data-product="${data.productId}"]`);
        if (cartItemElement) {
            var cartItemQuantityElement = cartItemElement.querySelector('.item-quantity');
            if (cartItemQuantityElement) {
                cartItemQuantityElement.innerText = data.itemQuantity;
            }

            var cartItemTotalElement = cartItemElement.querySelector('.item-total');
            if (cartItemTotalElement) {
                cartItemTotalElement.innerText = formatCurrency(data.itemQuantity * data.productPrice) + ' ₫';
            }

            if (data.itemQuantity <= 0 || data.action === 'remove_all') {  // Đảm bảo xóa mục nếu hành động là 'remove_all'
                cartItemElement.remove();
            }
        }
    }

    setupEventListeners();

    var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    var showLoginModalButtons = document.querySelectorAll('.show-login-modal');
    
    showLoginModalButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            loginModal.show();
        });
    });

    $(document).ready(function() {
        $('#edit-profile-btn').click(function() {
            $('#edit-profile-form').toggle();
            $('#edit-profile-btn').toggle();
        });
    });

    document.getElementById('cancel-edit-btn').addEventListener('click', function() {
        // Chuyển hướng người dùng về tab thông tin hồ sơ
        document.getElementById('profile-tab-link').click();
    });
});
