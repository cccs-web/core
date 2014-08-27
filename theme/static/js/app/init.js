// init DEBUG mode globally
if (typeof DEBUG === 'undefined') DEBUG = true;

// RequireJS config object -- Desktop devices
requirejs.config({
    baseUrl : '/static/js'

    , paths : {
        // jQuery
        'jquery':                       ['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery', 'libs/jquery']
		, 'jCookie':                    ['http://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.0/jquery.cookie.min', 'libs/jquery.cookie']
		, 'jEvtMove':                   ['libs/jquery.event.move']
        , 'jEvtSwipe':                  ['libs/jquery.event.swipe']
        , 'jVelocity':                  ['libs/jquery.velocity']
        , 'velocityUI':                 ['app/utils/velocity.fx']

        // Backbone - Marionette specific libs            
        , 'underscore':                 ['http://cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.min', 'libs/lodash']
        , 'backbone':                   ['http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min', 'libs/backbone']
        , 'marionette':                 ['http://cdnjs.cloudflare.com/ajax/libs/backbone.marionette/1.6.4-bundled/backbone.marionette.min', 'libs/backbone.marionette']
        , 'json':                       ['http://cdnjs.cloudflare.com/ajax/libs/json2/20130526/json2.min', 'libs/json2']
        , 'text':                       ['http://cdnjs.cloudflare.com/ajax/libs/require-text/2.0.12/text', 'libs/text']

        /* vendor scripts */
        , 'modernizr':                  ['http://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.2/modernizr.min','libs/modernizr']
        , 'fastclick':                  ['http://cdnjs.cloudflare.com/ajax/libs/fastclick/1.0.0/fastclick.min', 'libs//fastclick']
        , 'placeholder':                ['http://cdnjs.cloudflare.com/ajax/libs/jquery-placeholder/2.0.7/jquery.placeholder.min', 'libs/placeholder']

        // Foundation 5.3.0
        , 'foundation.core':            ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.min','libs/foundation/components/foundation']
        , 'foundation.abide':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.abide.min','libs/foundation/foundation.abide']
        , 'foundation.accordion':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.accordion.min','libs/foundation/foundation.accordion']
        , 'foundation.alert':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.alert.min','libs/foundation/foundation.alert']
        , 'foundation.clearing':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.clearing.min','libs/foundation/foundation.clearing']
        , 'foundation.dropdown':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.dropdown.min','libs/foundation/foundation.dropdown']
        , 'foundation.equalizer':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.equalizer.min','libs/foundation/foundation.equalizer']
        , 'foundation.interchange':     ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.interchange.min','libs/foundation/foundation.interchange']
        , 'foundation.joyride':         ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.joyride.min','libs/foundation/foundation.joyride']
        , 'foundation.magellan':        ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.magellan.min','libs/foundation/foundation.magellan']
        , 'foundation.offcanvas':       ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.offcanvas.min','libs/foundation/foundation.offcanvas']
        , 'foundation.orbit':           ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.orbit.min','libs/foundation/foundation.orbit']
        , 'foundation.reveal':          ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.reveal.min','libs/foundation/foundation.reveal']
        , 'foundation.slider':          ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.1/js/foundation/foundation.slider.min','libs/foundation/foundation.reveal']
        , 'foundation.tab':             ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.tab.min','libs/foundation/foundation.tab']
        , 'foundation.tooltip':         ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.tooltip.min','libs/foundation/foundation.tooltip']
        , 'foundation.topbar':          ['http://cdnjs.cloudflare.com/ajax/libs/foundation/5.3.0/js/foundation/foundation.topbar.min','libs/foundation/foundation.topbar']

        // HTML5 polyfills
        , 'yepnope' :                   ['http://cdnjs.cloudflare.com/ajax/libs/yepnope/1.5.4/yepnope.min','libs/yepnope']
        , 'html5shiv' :                 ['http://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7/html5shiv.min','libs/html5shiv']
        , 'nwmatcher' :                 ['http://cdnjs.cloudflare.com/ajax/libs/nwmatcher/1.2.5/nwmatcher.min','libs/nwmatcher']
        , 'selectivizr' :               ['http://cdnjs.cloudflare.com/ajax/libs/selectivizr/1.0.2/selectivizr-min','libs/selectivizr']
        , 'respond' :                   ['http://cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/respond','libs/respond']
        , 'css3pie' :                   ['http://cdnjs.cloudflare.com/ajax/libs/css3pie/2.0beta1/PIE_IE678','libs/css3pie']
        , 'svg' :                       ['libs/svg']
        , 'rem' :                       ['libs/rem']
        , 'dom_shim' :                  ['libs/DOM-shim']
        , 'event_helpers' :             ['libs/EventHelpers']
        , 'css_query' :                 ['libs/cssQuery-p']
        , 'sylvester' :                 ['libs/sylvester']
        , 'css_sandpaper' :             ['libs/cssSandpaper']

        // Application
        , 'app' :                       'app/app'
        , 'browser_check' :             'app/utils/browser_check'
        , 'dom_manipulation' :          'app/utils/dom_manipulation'
        , 'rgba' :                      'app/utils/ie-rgba'

    }

    , shim : {

        // Modernizr
        'modernizr' :                   { exports: 'Modernizr'}

        // jQuery Cookie
        , 'jCookie' :                   { deps: ['jquery'] }
        // , 'velocityUI':                 { deps: ['jquery', 'jVelocity'] }
        // , 'jVelocity':                  { deps: ['jquery'] } 

        // Fastclick
        , 'fastclick' :                 { exports: 'FastClick'}

        // Placeholder
        , 'placeholder' :               { exports: 'Placeholders'}

        // HTML5 polyfills
        , 'yepnope' :                   { deps : ['modernizr'] }
        , 'html5shiv' :                 { deps : ['modernizr'] }
        , 'nwmatcher' :                 { deps : ['modernizr'] }
        , 'selectivizr' :               { deps : ['modernizr'] }
        , 'respond' :                   { deps : ['modernizr'] }
        , 'css3pie' :                   { deps : ['modernizr'] }
        , 'svg' :                       { deps : ['modernizr'] }
        , 'rem' :                       { deps : ['modernizr'] }
        , 'dom_shim' :                  { deps : ['modernizr'] }
        , 'event_helpers' :             { deps : ['modernizr'] }
        , 'css_query' :                 { deps : ['modernizr'] }
        , 'sylvester' :                 { deps : ['modernizr'] }
        , 'css_sandpaper' :             { deps : ['modernizr'] }

        // Underscore (lodash)
        , 'underscore' :                { exports: '_' }
        
        // Backbone
        , 'backbone' :                  { deps: ['jquery', 'underscore', 'json'], exports: 'Backbone' }
        
        // Marionette
        , 'marionette' :                { deps: ['backbone'], exports: 'Marionette' }
        
        // Text
        , 'text':                       { deps: ['jquery'] }

        // Foundation 5
        , 'foundation.core':            { deps: ['modernizr','jquery'], exports: 'Foundation' }
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
        , 'foundation.slider':          { deps: ['foundation.core'] }
        , 'foundation.tab':             { deps: ['foundation.core'] }
        , 'foundation.tooltip':         { deps: ['foundation.core'] }
        , 'foundation.topbar':          { deps: ['foundation.core'] }
        
    }

    , deps : ['app']
    
    // the duration that require should wait before abandoning the load
    , waitSeconds : 300
    
    // prevents caching during development
    , urlArgs : 'ver=1.0-' + ((new Date()).getTime())
});
