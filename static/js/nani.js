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
// Ajax xử lý phân trang
