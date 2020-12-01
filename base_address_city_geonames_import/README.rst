=================================
Base Address City Geonames Import
=================================

.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

This module adds a wizard to import cities and/or city zip entries from
`Geonames <http://www.geonames.org/>`_ database. It is an alternative to the OCA module **base_location_geonames_import** from the OCA project `partner-contact <geonames-import-simple>`_. The main advantage of the module **base_address_city_geonames_import** is that it doesn't depend on the module *base_location* which adds an unnecessary object *res.city.zip* (that object is not necessary, the *res.city* object from the module *base_address_city* is enough).

Configuration
=============

To access the menu to import city zip entries from Geonames
you must add yourself to the groups *Administration / Settings* or, if you have sale module
installed, *Sales / Manager* group.

If you want/need to modify the default URL
(http://download.geonames.org/export/zip/), you can set the *geonames.url*
system parameter.

Usage
=====

Go to *Contacts > Configuration > Localization > Import from Geonames*,
and click on it to open a wizard.

When you start the wizard, it will ask you to select one or several countries.

Then, for the selected country, it will delete all not detected entries, download
the latest version of the list of cities from geonames.org and create new
city zip entries.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/akretion/geonames-import-simple/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/akretion/geonames-import-simple/issues/new?body=module:%20base_address_city_geonames_import%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Akretion
* Agile Business Group
* Tecnativa
* AdaptiveCity

Contributors
~~~~~~~~~~~~

* Alexis de Lattre <alexis.delattre@akretion.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Dave Lasley <dave@laslabs.com>
* Jordi Ballester <jordi.ballester@eficent.com>
* Franco Tampieri <franco@tampieri.info>
* Aitor Bouzas <aitor.bouzas@adaptivecity.com>
* Manuel Regidor <manuel.regidor@sygel.es>

Maintainers
~~~~~~~~~~~

This module is maintained by `Akretion <https://akretion.com/en>`_.
