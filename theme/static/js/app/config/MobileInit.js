// RequireJS config object  -- Touch devices
requirejs.config({
    baseUrl : './js'

    , paths : {
        // jQuery
        'jquery':                      ['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery', 'libs/jquery']
		, 'jCookie':                   ['http://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.0/jquery.cookie.min', 'libs/jquery.cookie']
		, 'jEvtMove':                  ['libs/jquery.event.move']
		, 'jEvtSwipe':                 ['libs/jquery.event.swipe']

        /* vendor scripts */
        , 'modernizr':                  ['http://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.2/modernizr.min', 'libs/modernizr']
        , 'fastclick':                  ['http://cdnjs.cloudflare.com/ajax/libs/fastclick/1.0.0/fastclick.min', 'libs/foundation/vendor/fastclick']
        , 'placeholder':                ['http://cdnjs.cloudflare.com/ajax/libs/jquery-placeholder/2.0.7/jquery.placeholder.min', 'libs/foundation/vendor/placeholder']

        // Foundation 5.3.0
        , 'foundation.core':            ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.min','libs/foundation/components/foundation']
        , 'foundation.abide':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.abide.min','libs/foundation/components/foundation.abide']
        , 'foundation.accordion':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.accordion.min','libs/foundation/components/foundation.accordion']
        , 'foundation.alert':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.alert.min','libs/foundation/components/foundation.alert']
        , 'foundation.clearing':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.clearing.min','libs/foundation/components/foundation.clearing']
        , 'foundation.dropdown':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.dropdown.min','libs/foundation/components/foundation.dropdown']
        , 'foundation.equalizer':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.equalizer.min','libs/foundation/components/foundation.equalizer']
        , 'foundation.interchange':     ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.interchange.min','libs/foundation/components/foundation.interchange']
        , 'foundation.joyride':         ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.joyride.min','libs/foundation/components/foundation.joyride']
        , 'foundation.magellan':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.magellan.min','libs/foundation/components/foundation.magellan']
        , 'foundation.offcanvas':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.offcanvas.min','libs/foundation/components/foundation.offcanvas']
        , 'foundation.orbit':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.orbit.min','libs/foundation/components/foundation.orbit']
        , 'foundation.reveal':          ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.reveal.min','libs/foundation/components/foundation.reveal']
        , 'foundation.tab':             ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.tab.min','libs/foundation/components/foundation.tab']
        , 'foundation.tooltip':         ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.tooltip.min','libs/foundation/components/foundation.tooltip']
        , 'foundation.topbar':          ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.topbar.min','libs/foundation/components/foundation.topbar']

        // Application
        , 'app':                       'app/app'
    }

    , shim : {

        // jQuery Cookie
        'jCookie':                      { deps: ['jquery'] }

        // Fastclick
        , 'fastclick':                  { exports: 'FastClick'}

        // Modernizr
        , 'modernizr':                  { exports: 'Modernizr'}

        // Placeholder
        , 'placeholder':                { exports: 'Placeholders'}

        // Foundation 5
        , 'foundation.core':            { deps: ['jquery', 'modernizr'], exports: 'Foundation' }
        , 'foundation.abide':           { deps: ['foundation.core'] }
        , 'foundation.accordion':       { deps: ['foundation.core'] }
        , 'foundation.alert':           { deps: ['foundation.core'] }
        , 'foundation.clearing':        { deps: ['foundation.core'] }
        , 'foundation.dropdown':        { deps: ['foundation.core'] }
        , 'foundation.equalizer':       { deps: ['foundation.core'] }
        , 'foundation.interchange':     { deps: ['foundation.core'] }
        , 'foundation.joyride':         { deps: ['foundation.core', 'jCookie'] }
        , 'foundation.magellan':        { deps: ['foundation.core'] }
        , 'foundation.offcanvas':       { deps: ['foundation.core'] }
        , 'foundation.orbit':           { deps: ['foundation.core'] }
        , 'foundation.reveal':          { deps: ['foundation.core'] }
        , 'foundation.tab':             { deps: ['foundation.core'] }
        , 'foundation.tooltip':         { deps: ['foundation.core'] }
        , 'foundation.topbar':          { deps: ['foundation.core'] }
    }

    , deps : ['app']
    
    // the duration that require should wait before abandoning the load
    , waitSeconds : 300
    
    // prevents caching during development (remove data and time for live app)
    , urlArgs : 'ver=1.0-' + ((new Date()).getTime())
});
