Author: Carl Kenny
Date:   26 July 2014
Usage:  python 404.py http://www.your.url.com x (-T/-F) > 404.txt
        - Where x is the max recursion depth. Remember that
          web is rather exponential, hence large x will be slow
        - (T/F) will accept either. T will only print dead links
          where as F will print both alive and dead links

Limits: Does not work for /relative_links and
        misses webpages with custom 404 pages' that have a
        url that doesn't end in /404/ - a RE could solve this
