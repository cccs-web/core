require(['modernizr'],
    function (Modernizr) {

        var BrowserDetect = {
            init: function () {
                this.browser = this.searchString(this.dataBrowser) || "Other";
                this.version = this.searchVersion(navigator.userAgent) || this.searchVersion(navigator.appVersion) || "Unknown";
            },

            searchString: function (data) {
                for (var i=0 ; i < data.length ; i++) {
                    var dataString = data[i].string;
                    this.versionSearchString = data[i].subString;

                    if (dataString.indexOf(data[i].subString) != -1) {
                        return data[i].identity;
                    }
                }
            },

            searchVersion: function (dataString) {
                var index = dataString.indexOf(this.versionSearchString);
                if (index == -1) return;
                return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
            },

            dataBrowser: [
                { string: navigator.userAgent, subString: "MSIE",    identity: "Explorer" },
                { string: navigator.userAgent, subString: "Firefox", identity: "Firefox" },
                { string: navigator.userAgent, subString: "Chrome",  identity: "Chrome" },
                { string: navigator.userAgent, subString: "Safari",  identity: "Safari" },
                { string: navigator.userAgent, subString: "Opera",   identity: "Opera" }
            ]
        };
        
        BrowserDetect.init();

        // We checkout if client is Explorer < 9 and give it some polyfills if so
        if (BrowserDetect.browser === "Explorer" && BrowserDetect.version < 9 ) require(['html5shiv','respond','selectivizr','css3pie']);

        // We checkout if client isn't capable of rendering svg
        if (!Modernizr.svg) require(['svg']);

        // We checkout if client isn't capable of rendering rem units
        if (!Modernizr.rem) require(['rem']);

        // We checkout if client isn't capable of rendering CSS3 tranform, box-shadow, gradients, opacity and RGBA/HSL/HSLA colours 
        if ((!Modernizr.csstransforms) || (!Modernizr.rgba) || (!Modernizr.cssgradients) || (!Modernizr.opacity) || (!Modernizr.boxshadow)) {
            require(['event_helpers','css_query','sylvester','css_sandpaper']);
        }
    }
);