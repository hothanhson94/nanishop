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

	// open your cart
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
	      },
	    ]
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
      },
    ]
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

	priceInputMax.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value)
	});

	priceInputMin.addEventListener('change', function(){
		updatePriceSlider($(this).parent() , this.value)
	});

	function updatePriceSlider(elem , value) {
		if ( elem.hasClass('price-min') ) {
			console.log('min')
			priceSlider.noUiSlider.set([value, null]);
		} else if ( elem.hasClass('price-max')) {
			console.log('max')
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

        initSlick('#laptops-tab1', '#slick1', '#slick-nav-1');
        initSlick('#smartphones-tab', '#slick2', '#slick-nav-2');
        initSlick('#cameras-tab', '#slick3', '#slick-nav-3');
        initSlick('#accessories-tab', '#slick4', '#slick-nav-4');
		initSlick('#laptops-tab5', '#slick5', '#slick-nav-5');
        initSlick('#smartphones-tab6', '#slick6', '#slick-nav-6');
        initSlick('#cameras-tab7', '#slick7', '#slick-nav-7');
        initSlick('#accessories-tab8', '#slick8', '#slick-nav-8');
    });

	// // Countdown
	// // Set the date we're counting down to
	// var countDownDate = new Date("Jun 26, 2025 15:37:25").getTime();

	// // Update the count down every 1 second
	// var countdownFunction = setInterval(function() {

	// 	// Get today's date and time
	// 	var now = new Date().getTime();

	// 	// Find the distance between now and the count down date
	// 	var distance = countDownDate - now;

	// 	// Time calculations for days, hours, minutes and seconds
	// 	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	// 	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	// 	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	// 	var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	// 	// Output the result in an element with id="days", "hours", "minutes", "seconds"
	// 	document.getElementById("days").innerHTML = days;
	// 	document.getElementById("hours").innerHTML = hours;
	// 	document.getElementById("minutes").innerHTML = minutes;
	// 	document.getElementById("seconds").innerHTML = seconds;

	// 	// If the count down is finished, write some text
	// 	if (distance < 0) {
	// 		clearInterval(countdownFunction);
	// 		document.querySelector(".hot-deal").innerHTML = "<h2 class='text-uppercase'>The deal has ended</h2>";
	// 	}
	// }, 1000);

})(jQuery);