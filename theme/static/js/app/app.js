require([
    'jquery'
    , 'modernizr'
    , 'fastclick'
    , 'foundation.abide'
    , 'foundation.accordion'
    , 'foundation.alert'
    , 'foundation.clearing'
    , 'foundation.dropdown'
    , 'foundation.equalizer'
    , 'foundation.interchange'
    , 'foundation.joyride'
    , 'foundation.magellan'
    , 'foundation.offcanvas'
    , 'foundation.orbit'
    , 'foundation.reveal'
    , 'foundation.slider'
    , 'foundation.tab'
    , 'foundation.tooltip'
    , 'foundation.topbar'
    , 'jVelocity'
    , 'velocityUI'
    , 'jCookie'

    ], function ($, Modernizr, FastClick) {

        // Initialize Foundation JS ( with optional configuration and overrides )
        $(document).foundation({
            reveal: {
                animation: 'fadeIn'
                , animation_speed: 250
            },

            // A set of global Joyride configuration options, 
            // They can also be overriden in particular HTML data-options attributes
            joyride: {
                expose                   : false,     // turn on or off the expose feature
                modal                    : true,      // Whether to cover page with modal during the tour
                tip_location             : 'bottom',  // 'top' or 'bottom' in relation to parent
                nub_position             : 'auto',    // override on a per tooltip bases
                scroll_speed             : 500,       // Page scrolling speed in milliseconds, 0 = no scroll animation
                scroll_animation         : 'swing',  // supports 'swing' and 'linear', extend with jQuery UI.
                timer                    : 3000,         // 0 = no timer , all other numbers = timer in milliseconds
                start_timer_on_click     : true,      // true or false - true requires clicking the first button start the timer
                start_offset             : 0,         // the index of the tooltip you want to start on (index of the li)
                next_button              : true,      // true or false to control whether a next button is used
                prev_button              : true,      // true or false to control whether a prev button is used
                tip_animation            : 'fade',    // 'pop' or 'fade' in each tip
                pause_after              : [],        // array of indexes where to pause the tour after
                exposed                  : [],        // array of expose elements
                tip_animation_fade_speed : 300,       // when tipAnimation = 'fade' this is speed in milliseconds for the transition
                cookie_monster           : false,     // true or false to control whether cookies are used
                cookie_name              : 'joyride', // Name the cookie you'll use
                cookie_domain            : false,     // Will this cookie be attached to a domain, ie. '.notableapp.com'
                cookie_expires           : 365,       // set when you would like the cookie to expire.
                tip_container            : 'body',    // Where will the tip be attached
                tip_location_patterns    : {
                    top: ['bottom'],
                    bottom: [], // bottom should not need to be repositioned
                    left: ['right', 'top', 'bottom'],
                    right: ['left', 'top', 'bottom']
                },
                post_ride_callback     : function (){},    // A method to call once the tour closes (canceled or complete)
                post_step_callback     : function (){},    // A method to call after each step
                pre_step_callback      : function (){},    // A method to call before each step
                pre_ride_callback      : function (){},    // A method to call before the tour starts (passed index, tip, and cloned exposed element)
                post_expose_callback   : function (){},    // A method to call after an element has been exposed
                template : { // HTML segments for tip layout
                    link        : '<a href="#close" class="joyride-close-tip">&times;</a>',
                    timer       : '<div class="joyride-timer-indicator-wrap"><span class="joyride-timer-indicator"></span></div>',
                    tip         : '<div class="joyride-tip-guide"><span class="joyride-nub"></span></div>',
                    wrapper     : '<div class="joyride-content-wrapper"></div>',
                    button      : '<a href="#" class="small button joyride-next-tip"></a>',
                    prev_button : '<a href="#" class="small button joyride-prev-tip"></a>',
                    modal       : '<div class="joyride-modal-bg"></div>',
                    expose      : '<div class="joyride-expose-wrapper"></div>',
                    expose_cover: '<div class="joyride-expose-cover"></div>'
                },
                expose_add_class : '' // One or more space-separated class names to be added to exposed element
            },

            orbit: {
                animation: 'slide', // Sets the type of animation used for transitioning between slides, can also be 'fade'
                timer_speed: 10000, // Sets the amount of time in milliseconds before transitioning a slide
                pause_on_hover: true, // Pauses on the current slide while hovering
                resume_on_mouseout: false, // If pause on hover is set to true, this setting resumes playback after mousing out of slide
                next_on_click: true, // Advance to next slide on click
                animation_speed: 500, // Sets the amount of time in milliseconds the transition between slides will last
                stack_on_small: false,
                navigation_arrows: true,
                slide_number: true,
                slide_number_text: 'of',
                container_class: 'orbit-container',
                stack_on_small_class: 'orbit-stack-on-small',
                next_class: 'orbit-next', // Class name given to the next button
                prev_class: 'orbit-prev', // Class name given to the previous button
                timer_container_class: 'orbit-timer', // Class name given to the timer
                timer_paused_class: 'paused', // Class name given to the paused button
                timer_progress_class: 'orbit-progress', // Class name given to the progress bar
                slides_container_class: 'orbit-slides-container', // Class name given to the slide container
                preloader_class: 'preloader', // Class given to the perloader
                slide_selector: 'li', // Default is '*' which selects all children under the container
                bullets_container_class: 'orbit-bullets',
                bullets_active_class: 'active', // Class name given to the active bullet
                slide_number_class: 'orbit-slide-number', // Class name given to the slide number
                caption_class: 'orbit-caption', // Class name given to the caption
                active_slide_class: 'active', // Class name given to the active slide
                orbit_transition_class: 'orbit-transitioning',
                bullets: true, // Does the slider have bullets visible?
                circular: true, // Does the slider should go to the first slide after showing the last?
                timer: true, // Does the slider have a timer active? Setting to false disables the timer.
                variable_height: false, // Does the slider have variable height content?
                swipe: true,
                // before_slide_change: noop, // Execute a function before the slide changes
                // after_slide_change: noop // Execute a function after the slide changes
            },

            slider: {
                start: 1,
                end: 10,
                on_change: function() {
                  // something when the value changes
              }
            },

            topbar: {
                sticky_class : 'sticky',
                custom_back_text: true, // Set this to false and it will pull the top level link name as the back text
                back_text: '..', // Define what you want your custom back text to be if custom_back_text: true
                is_hover: true,
                mobile_show_parent_link: false, // will copy parent links into dropdowns for mobile navigation
                scrolltop : true // jump to top when sticky nav menu toggle is clicked
            }
        });

        // launch the joyride - needs a special init call
        // $(document).foundation('joyride','start');

        // open a modal when page loads
        // $('#welcome').foundation('reveal', 'open');

        // Now that Foundation has loaded everything I want to: 
        // set new .clearing-thumbs inline style without touching the foundation component
        $(document.body).on("opened.fndtn.clearing", function(event) {
            if (DEBUG) console.info("opened thumbnail with src ", $('img', event.target).attr('src'));
            $('.clearing-thumbs').css('width','auto');
        });

        // Testing Velocity.js
        // $("header").velocity("callout.shake");
        // $('header').velocity("transition.shrinkOut");
        // $('header').velocity("transition.shrinkIn");

        // setInterval(function() {
        //     $('.icon-bar').velocity("callout.pulse");
        // }, 2000);

            
        // Topbar
        var
            w = $(window).width(),
            tlh = $('.top-bar').height();

        $('#search').click(function(e) {
            e.preventDefault();
            $(this).toggleClass('active');
            $('.search').toggleClass('visible');
            $('.search ul').slideToggle('fast');
        });

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
    }
);