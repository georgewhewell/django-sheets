=============================
django-sheets
=============================

Use Google Sheets as context variables in Django templates

.. image:: https://badge.fury.io/py/django-sheets.png
    :target: https://badge.fury.io/py/django-sheets

.. image:: https://travis-ci.org/georgewhewell/django-sheets.png?branch=master
    :target: https://travis-ci.org/georgewhewell/django-sheets

.. image:: https://coveralls.io/repos/georgewhewell/django-sheets/badge.png?branch=master
    :target: https://coveralls.io/r/georgewhewell/django-sheets?branch=master
    
.. image:: https://requires.io/github/georgewhewell/django-sheets/requirements.svg?branch=master
     :target: https://requires.io/github/georgewhewell/django-sheets/requirements/?branch=master
     :alt: Requirements Status

Usage
_____________

In your template::

    {% load sheets %}
    {% csv "1uPsdcGUnUsf3d2xGHRGUUb7_k5IQPtBvfQY61u8Z8wE" as csv_data %}
    <table>
    {% for row in csv_data %}
        <tr>
        {% for cell in row %}
            <td>{{ cell }}</td>
        {% endfor %}
        </td>
    </table>
    {% endfor %}

View the output, you should see

=================================  =======================  ===============  =======================
Origin (English)                   Name (English)           Origin (Native)  Name (Native)
Australia                          Nicole Kidman            Australia        Nicole Kidman
Austria                            Johann Strauss           Österreich       Johann Strauß
Belgium (Flemish)                  Rene Magritte            België           René Magritte
Belgium (French)                   Rene Magritte            Belgique         René Magritte
Belgium (German)                   Rene Magritte            Belgien          René Magritte
=================================  =======================  ===============  =======================



Documentation
-------------

Documentation is available at https://django-sheets.readthedocs.org.
