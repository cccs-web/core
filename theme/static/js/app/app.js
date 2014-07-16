require([
    'jquery'
    , 'modernizr'
    , 'yepnope'
    , 'browser-detect'
    , 'fastclick'
    // , 'text'
    // , 'foundation.abide'
    // , 'foundation.accordion'
    , 'foundation.alert'
    // , 'foundation.clearing'
    // , 'foundation.dropdown'
    // , 'foundation.equalizer'
    , 'foundation.interchange'
    // , 'foundation.joyride'
    // , 'foundation.magellan'
    // , 'foundation.offcanvas'
    // , 'foundation.orbit'
    , 'foundation.reveal'
    // , 'foundation.tab'
    , 'foundation.tooltip'
    // , 'foundation.topbar'

    // , 'bs.affix'
    // , 'bs.alert'
    // , 'bs.button'
    // , 'bs.carousel'
    // , 'bs.collapse'
    // , 'bs.dropdown'
    // , 'bs.modal'
    // , 'bs.popover'
    // , 'bs.scrollspy'
    // , 'bs.tab'
    // , 'bs.tooltip'
    // , 'bs.transition'

    ], function ($, Modernizr, FastClick) {

        // Initialize Foundation JS ( with optional configuration )
        $(document).foundation({
            reveal: {
                animation: 'fadeIn'
                , animation_speed: 500
            }
        });

        // Howto open a modal when page loads
        $('#welcome').foundation('reveal', 'open');

        // Modernizr for browser media queries support
        if (Modernizr.mq('only all')) {
            console.log('mq ok  ');
        } else {
            console.log('we could have a polyfill for this');
            // eg.  define(['mqfix','html5shiv','etc'],function($,Modernizr,etc){})
            // or require(['polyfill1,2,...'],function(polyfill1,2,...){});
        }

        if (DEBUG) console.log('rem unit: '+Modernizr.cssremunit);

        // YepNope / Modernizr test for rem an mq, trying this too
        yepnope([
            {
                test: Modernizr.cssremunit
                , yep: function() {
                    if (DEBUG) alert('yep, this is rem capable');
                }
                , nope: ['libs/rem.js']
                , complete: function(url,result,key) {
                    if (DEBUG) alert('oh we loaded the rem unit polyfill');
                }
            }
            , {
                test: Modernizr.mq 
                , yep: function() {
                    if (DEBUG) console.log('yep, mq works too');
                }
                , nope: ['libs/respond.js']
                , complete: function(url,result,key) {
                    if (DEBUG) alert('had to load the mq polyfill');
                }
            }
        ]);
    }
);