// init DEBUG mode globally
if (typeof DEBUG === 'undefined') DEBUG = true;

// RequireJS config object -- Desktop devices
requirejs.config({
    baseUrl : '/static/js'

    , paths : {
        // jQuery
        'jquery':                      ['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery', 'libs/jquery']
		, 'jCookie':                   ['http://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.0/jquery.cookie.min', 'libs/jquery.cookie']
		, 'jEvtMove':                  ['libs/jquery.event.move']
		, 'jEvtSwipe':                 ['libs/jquery.event.swipe']

        // Backbone - Marionette specific libs            
        // , underscore:                ['http://cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.min', 'libs/lodash']
        // , backbone:                  ['http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min', 'libs/backbone']
        // , marionette:                ['http://cdnjs.cloudflare.com/ajax/libs/backbone.marionette/1.6.4-bundled/backbone.marionette.min', 'libs/backbone.marionette']
        // , json:                      ['http://cdnjs.cloudflare.com/ajax/libs/json2/20130526/json2.min', 'libs/json2']
        , text:                         ['http://cdnjs.cloudflare.com/ajax/libs/require-text/2.0.12/text', 'libs/text']

        /* vendor scripts */
        , 'modernizr':                  ['libs/modernizr']
        , 'fastclick':                  ['http://cdnjs.cloudflare.com/ajax/libs/fastclick/1.0.0/fastclick.min', 'libs//fastclick']
        , 'placeholder':                ['http://cdnjs.cloudflare.com/ajax/libs/jquery-placeholder/2.0.7/jquery.placeholder.min', 'libs/placeholder']

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

        // Bootstrap 3.2.0
        , 'bs.affix' :                  ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/affix.min','libs/bootstrap/affix']
        , 'bs.alert' :                  ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/alert.min','libs/bootstrap/alert']
        , 'bs.button' :                 ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/button.min','libs/bootstrap/button']
        , 'bs.carousel' :               ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/carousel.min','libs/bootstrap/carousel']
        , 'bs.collapse' :               ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/collapse.min','libs/bootstrap/collapse']
        , 'bs.dropdown' :               ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/dropdown.min','libs/bootstrap/dropdown']
        , 'bs.modal' :                  ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/modal.min','libs/bootstrap/modal']
        , 'bs.popover' :                ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/popover.min','libs/bootstrap/popover']
        , 'bs.scrollspy' :              ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/scrollspy.min','libs/bootstrap/scrollspy']
        , 'bs.tab' :                    ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/tab.min','libs/bootstrap/tab']
        , 'bs.tooltip' :                ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/tooltip.min','libs/bootstrap/tooltip']
        , 'bs.transition' :             ['http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/transition.min','libs/bootstrap/transition']


        // HTML5 polyfills for getting IE7 and IE8 work with Foundation5
        , 'yepnope' :                   ['http://cdnjs.cloudflare.com/ajax/libs/yepnope/1.5.4/yepnope.min','libs/yepnope']
        , 'html5shiv' :                 ['http://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7/html5shiv.min','libs/html5shiv']
        , 'nwmatcher' :                 ['http://cdnjs.cloudflare.com/ajax/libs/nwmatcher/1.2.5/nwmatcher.min','libs/nwmatcher']
        , 'selectivizr' :               ['http://cdnjs.cloudflare.com/ajax/libs/selectivizr/1.0.2/selectivizr-min','libs/selectivizr']
        , 'respond' :                   ['http://cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/respond','libs/respond']
        , 'css3pie' :                   ['http://cdnjs.cloudflare.com/ajax/libs/css3pie/2.0beta1/PIE_IE678','libs/css3pie']

        // Application
        , 'app' :                       'app/app'
        , 'browser-detect' :            'app/utils/browser-detect'

    }

    , shim : {

        // jQuery Cookie
        'jCookie' :                      { deps: ['jquery'] }

        // Fastclick
        , 'fastclick' :                  { exports: 'FastClick'}

        // Modernizr
        , 'modernizr' :                  { exports: 'Modernizr'}

        // Placeholder
        , 'placeholder' :                { exports: 'Placeholders'}

        // HTML5 polyfills - IE8 fixes
        , 'yepnope' :                   { deps : ['modernizr'] }

        // Underscore (lodash)
        // 'underscore' :               { exports: '_' }
        
        // Backbone
        // , 'backbone' :               { deps: ['jquery', 'underscore', 'json'], exports: 'Backbone' }
        
        // Marionette
        // , 'marionette' :             { deps: ['backbone'], exports: 'Marionette' }
        
        // Text
        , 'text':                       { deps: ['jquery'] }

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
        
        // Boostrap 3
        , 'bs.affix':      { deps: ['jquery'], exports: '$.fn.affix' }
        , 'bs.alert':      { deps: ['jquery'], exports: '$.fn.alert' }
        , 'bs.button':     { deps: ['jquery'], exports: '$.fn.button' }
        , 'bs.carousel':   { deps: ['jquery'], exports: '$.fn.carousel' }
        , 'bs.collapse':   { deps: ['jquery'], exports: '$.fn.collapse' }
        , 'bs.dropdown':   { deps: ['jquery'], exports: '$.fn.dropdown' }
        , 'bs.modal':      { deps: ['jquery'], exports: '$.fn.modal' }
        , 'bs.popover':    { deps: ['jquery', 'bs.tooltip'], exports: '$.fn.popover' }
        , 'bs.scrollspy':  { deps: ['jquery'], exports: '$.fn.scrollspy' }
        , 'bs.tab':        { deps: ['jquery'], exports: '$.fn.tab' }
        , 'bs.tooltip':    { deps: ['jquery'], exports: '$.fn.tooltip' }
        , 'bs.transition': { deps: ['jquery'], exports: '$.fn.transition' }
    }

    , deps : ['app']
    
    // the duration that require should wait before abandoning the load
    , waitSeconds : 300
    
    // prevents caching during development
    , urlArgs : 'ver=1.0-' + ((new Date()).getTime())
});
