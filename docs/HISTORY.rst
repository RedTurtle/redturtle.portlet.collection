Changelog
=========

2.0.0 (2022-07-14)
------------------

- major refactoring for python 3.8 and plone 5.2.
  [reflab]

1.0 (08/12/2019)
----------------

- update metadata in setup.py and history
  [lucabel]

1.0.0 (11/10/2017)
------------------

- Plone 5 compatibility. For Plone < 5 use 0.x versions
  [cekk]


0.6 (2017-01-26)
----------------

- skip first n element
  [mamico]


0.5 (2015-02-17)
----------------

- Now compatible with the new feature introduced with plone.portlet.collection 2.1.6
  (shipped with Plone 4.3.4)
  [keul]
- Do not display "None" CSS class
  [keul]
- Image grabbing works also for Plone sites not in the VHM root
  [keul]
- Add reference field relate to images; in this way user it's able to add header image to collection
  [lucabel]
- Fix rss icon
  [lucabel]
- Added italian portlet name translation
  [lucabel]

0.4 (2013-07-31)
----------------

- Added custom permission to add the portlet [cekk]

0.3 (2012-09-20)
----------------

* reverted changes done in version 0.3a because lead to issues on Plone 4.2.
  Re-fixed for Plone 4.2/Chameleon in the "old way"
  [keul]
* added a proper uninstall procedure
  [keul]
* pyflakes cleanup
  [keul]

0.3a (2012/06/13)
-----------------

* compatibility with Plone 4.2rc2 [amleczko]

0.2.11 (2012/03/19)
-------------------

* added rss_url method that return the right RSS feed url for the collection [micecchi]

0.2.10 (2011/10/10)
-------------------

* added control in template for no-more existing collection [micecchi]

0.2.9 (2011/08/31)
------------------

* included plone.app.portlets package [micecchi]

0.2.8 (2011/08/30)
------------------

* fixed "more..." link also in the header [micecchi]

0.2.7 (2011/08/29)
------------------

* Fixed RSS icon field in the example template [keul]
* Added reference field for "more..." link [micecchi]

0.2.6 (2011-07-21)
------------------

* changed edit_permission to "ManagePortlets" [micecchi]

0.2.5 (2011-04-05)
------------------

* New egg. The last was corrupted [micecchi]

0.2.4 (2011-04-04)
------------------

* Fixed project URL
* Added CSS style field [micecchi]
* Added translations [micecchi]

0.2.3 (2010-10-22)
------------------

* z3c.autoinclude support [keul]
* First public release [keul]

0.2.2
-----

* Some fix to the base skin template and also to the default skins template

0.2.1
-----

* BUG: The "more..." link was not show if the "no element" text was used

0.2.0
-----

* You can (must!) now choose a skins template to use with the portlet

0.1.3
-----

* Modification to get XHTML Strict code
