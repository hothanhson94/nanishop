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

