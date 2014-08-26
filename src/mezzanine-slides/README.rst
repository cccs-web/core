mezzanine-slides
================

Add simple slide functionality to your Mezzanine based website allowing for
beautiful banners at the tops of pages.


Setup
-----

1. Run ``pip install mezzanine-slides``
2. In ``settings.py`` add ``mezzanine_slides`` to your ``INSTALLED_APPS`` above
   mezzanine apps.
3. Run createdb or syncdb, if running syncdb run migrate if you are using South.
4. Modify your ``base.html`` template as described below.


Templates
---------

We have two template options, fullscreen slides or standard slides. Include
only one of the templates, css and js.


Standard Slides
===============

Add this to ``base.html`` where you would like the slides to appear::

  {% include "includes/standard_slides.html" %}

Include the CSS and JS in the compress areas of the ``base.html`` template::

  {% compress css %}
  ...
  <link rel="stylesheet" href="{% static "responsiveslides/responsiveslides.css" %}"/>
  {% endcompress %}

  {% compress js %}
  ...
  <script src="{% static "responsiveslides/responsiveslides.min.js" %}"></script>
  {% endcompress %}


Fullscreen Slides
==================

Add this to ``base.html`` where you would like the slides to appear::

  {% include "includes/fullscreen_slides.html" %}

Include the CSS and JS in the compress areas of the ``base.html`` template::

  {% compress css %}
  ...
  <link rel="stylesheet" href="{% static "vegas/jquery.vegas.min.css" %}"/>
  {% endcompress %}

  {% compress js %}
  ...
  <script src="{% static "vegas/jquery.vegas.min.js" %}"></script>
  {% endcompress %}


Credits
-------

Thanks to `Viljami Salminen`_ for `ResponsiveSlides.js`_ plugin and
`Jay Salvat`_ for `Vegas Background jQuery Plugin`_.

PWhipp: Enhanced to support Python 3


.. Links

.. _Viljami Salminen: http://viljamis.com/
.. _ResponsiveSlides.js: http://responsive-slides.viljamis.com/
.. _Jay Salvat: http://jaysalvat.com/
.. _Vegas Background jQuery Plugin: http://vegas.jaysalvat.com/

