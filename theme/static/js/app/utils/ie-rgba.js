define(['jquery']
	, function($) {

		function ieRGBA(rr, gg, bb, aa) {
		    'use strict';
		    
		    /* @rr, @gg, @bb (Integer) Color value - 0 to 255 @aa (Float) Opacity - 0 to 1 eg. 0.5 returns: #AARRGGBB (Hex String) */

		    return '#' + [
		        parseInt(aa * 255, 10).toString(16),
		        ('00' + (rr).toString(16)).slice(-2),
		        ('00' + (gg).toString(16)).slice(-2),
		        ('00' + (bb).toString(16)).slice(-2)
		    ].join('').toUpperCase();
		}

		var rgba = ieRGBA(11, 115, 85, 0.6925),
		hex = document.getElementsByClassName('columns');

		hex[0].innerHTML = rgba;
		hex[1].innerHTML = rgba;
		hex[2].innerHTML = rgba;
	}
);