========
Usage
========

To use django-sheets, you need to have a key to a publically-accessible 
Google Sheets spreadsheet. To find it, open your sheet and select
File -> Publish to the web.

Press Share, and select the link. You'll find the 44-character key as
part of the link. For example, the sample link:

https://docs.google.com/spreadsheets/d/**1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM**/pubhtml

Load the django-sheets template tags in your template::

    {% load sheets %}

Assign the CSV data to a variable using the ``{% csv %}`` tag::

    {% csv <key> as <variable_name> %}

Try it using the sample key above::

    {% load sheets %}
    {% csv "1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM" as uk500 %}
    <table>
    {% for row in uk500 %}
        <tr>
        {% for cell in row %}
            <td>{{ cell }}</td>
        {% endfor %}
        </td>
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
