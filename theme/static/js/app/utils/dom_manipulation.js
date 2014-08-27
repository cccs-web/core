require(['modernizr', 'jquery'],
    function (Modernizr, $) {
    	"use strict";
    	
        // Topbar
        var
            w = $(window).width(),
            tlh = $('.top-bar').height();

        // Search form
        // toggle the search form visibility on click interaction
        $('#search').click(function(e) {
            e.preventDefault();
            $(this).toggleClass('active');
            $('.search').toggleClass('visible');
            ( $('.search.visible').length > 0 ) ? $('.search').slideDown('fast').find('ul').slideDown('fast') : $('.search').slideUp('fast').find('ul').slideUp('fast');
        });

        // watch the scroll position and toggle the search form accordingly
        $(window).scroll(function() {
            if ($(this).scrollTop() <= 1) {
                $('#search').addClass('active');
                $('.search').addClass('visible').slideDown('fast');
                $('.search ul').slideDown('fast');
                $('.top-bar').removeClass('scrolling');
                return;
            }
            if ($(this).scrollTop() > 100) {
                $('#search').removeClass('active');
                $('.search ul').slideUp('fast');
                $('.search').removeClass('visible').slideUp('fast');
                $('.top-bar').addClass('scrolling');
                return;
            } else {
                return;
            }
        });

        // check input radio values in the search form
        $('#search_form input').on('change', function() {
	        if ( $('input[name="type"]:checked').length > 0 ) {
		       $(this).closest('dl').find('dd').removeClass('active');
		       $(this).closest('dd').addClass('active');
	        }
		});



        // Testing Velocity.js
        // $("header").velocity("callout.shake");
        // $('header').velocity("transition.shrinkOut");
        // $('header').velocity("transition.shrinkIn");

        // setInterval(function() {
        //     $('.icon-bar').velocity("callout.pulse");
        // }, 2000);


        // Search form
        
    }
);