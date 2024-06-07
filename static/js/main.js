(function($) {
    "use strict"

    // Mobile Nav toggle
    $('.menu-toggle > a').on('click', function (e) {
        e.preventDefault();
        $('#responsive-nav').toggleClass('active');
    })

    // Fix cart dropdown from closing
    $('.cart-dropdown').on('click', function (e) {
        e.stopPropagation();
    });

    // Open your cart
    $(document).ready(function() {
        $('.dropdown-toggle').on('click', function(event) {
            event.preventDefault();
            var $dropdown = $(this).closest('.dropdown');
            $dropdown.toggleClass('open');
        });

        $(document).on('click', function(event) {
            if (!$(event.target).closest('.dropdown').length) {
                $('.dropdown').removeClass('open');
            }
        });
    });

    /////////////////////////////////////////

    // Products Slick
    $('.products-slick').each(function() {
        var $this = $(this),
            $nav = $this.attr('data-nav');

        $this.slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            infinite: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
            responsive: [{
                breakpoint: 991,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }]
        });
    });

    // Products Widget Slick
    $('.products-widget-slick').each(function() {
        var $this = $(this),
            $nav = $this.attr('data-nav');

        $this.slick({
            infinite: true,
            autoplay: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
        });
    });

    /////////////////////////////////////////

    // Product Main img Slick
    $('#product-main-img').slick({
        infinite: true,
        speed: 300,
        dots: false,
        arrows: true,
        fade: true,
        asNavFor: '#product-imgs',
    });

    // Product imgs Slick
    $('#product-imgs').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: true,
        centerMode: true,
        focusOnSelect: true,
        centerPadding: 0,
        vertical: true,
        asNavFor: '#product-main-img',
        responsive: [{
            breakpoint: 991,
            settings: {
                vertical: false,
                arrows: false,
                dots: true,
            }
        }]
    });

    // Product img zoom
    var zoomMainProduct = document.getElementById('product-main-img');
    if (zoomMainProduct) {
        $('#product-main-img .product-preview').zoom();
    }

    /////////////////////////////////////////

    // Input number
    $('.input-number').each(function() {
        var $this = $(this),
            $input = $this.find('input[type="number"]'),
            up = $this.find('.qty-up'),
            down = $this.find('.qty-down');

        down.on('click', function () {
            var value = parseInt($input.val()) - 1000000;
            value = value < 100000 ? 100000 : value;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value)
        })

        up.on('click', function () {
            var value = parseInt($input.val()) + 1000000;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value)
        })
    });

    var priceInputMax = document.getElementById('price-max'),
        priceInputMin = document.getElementById('price-min');

    if (priceInputMax) {
        priceInputMax.addEventListener('change', function(){
            updatePriceSlider($(this).parent() , this.value)
        });
    }

    if (priceInputMin) {
        priceInputMin.addEventListener('change', function(){
            updatePriceSlider($(this).parent() , this.value)
        });
    }

    function updatePriceSlider(elem , value) {
        if ( elem.hasClass('price-min') ) {
            priceSlider.noUiSlider.set([value, null]);
        } else if ( elem.hasClass('price-max')) {
            priceSlider.noUiSlider.set([null, value]);
        }
    }

    // Price Slider
    var priceSlider = document.getElementById('price-slider');
    if (priceSlider) {
        noUiSlider.create(priceSlider, {
            start: [100000, 50000000],
            connect: true,
            step: 1000000,
            range: {
                'min': 100000,
                'max': 50000000
            }
        });

        priceSlider.noUiSlider.on('update', function( values, handle ) {
            var value = values[handle];
            handle ? priceInputMax.value = value : priceInputMin.value = value
        });
    }

    // Slicks slider
    $(document).ready(function(){
        function initSlick(tabId, slickId, navId) {
            $(tabId).on('shown.bs.tab', function () {
                $(slickId).not('.slick-initialized').slick({
                    slidesToShow: 4,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    dots: false,
                    prevArrow: '<button type="button" class="slick-prev">Previous</button>',
                    nextArrow: '<button type="button" class="slick-next">Next</button>',
                    appendArrows: navId,
                    responsive: [
                        {
                            breakpoint: 768,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 1
                            }
                        },
                        {
                            breakpoint: 480,
                            settings: {
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        }
                    ]
                });
            }).trigger('shown.bs.tab'); // Ensure the first tab initializes Slick
        }

        initSlick('#dien-thoai-tab1', '#slick1', '#slick-nav-1');
        initSlick('#laptop-tab2', '#slick2', '#slick-nav-2');
        initSlick('#tablet-tab3', '#slick3', '#slick-nav-3');
        initSlick('#phu-kien-tab4', '#slick4', '#slick-nav-4');
        initSlick('#dien-thoai-tab5', '#slick5', '#slick-nav-5');
        initSlick('#laptop-tab6', '#slick6', '#slick-nav-6');
        initSlick('#tablet-tab7', '#slick7', '#slick-nav-7');
        initSlick('#phu-kien-tab8', '#slick8', '#slick-nav-8');
    });
})(jQuery);
