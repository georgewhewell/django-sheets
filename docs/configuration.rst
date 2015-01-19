============
Configuration
============

Provided your Django project has a working cache backend, django-sheets will cache requests to the Google Sheets API for 5 minutes.

 - Performance- making an extra HTTP request per page-view (or more) will lead to poor response times.
 - Reliability- The Google Sheets API may experience failing requests- having a cached copy on your servers means this is less likely to affect you.
 - Exceeding quota- By making excessive requests you risk exceeding the API Quota and having requests denied until the quota is refreshed, making your page unusable.

If you wish to disable this cache, add to your settings file::

    SHEETS_CACHE_DISABLED = True

You can lower the cache timeout if you wish to sacrifice performance to lessen the chance of stale data, or extend it to improve performance and reduce server load::

    # Set timeout to 1 hour
    SHEETS_CACHE_TIMEOUT = 3600