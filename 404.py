import urllib
import urllib2
import sys
from BeautifulSoup import BeautifulSoup

"""
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
"""

def returnCode(url, happyLinks, deadLinks):
    """
    //TODO: Currently the script considers 're-directs' as 404
    :return:    happyLinks, deadLinks
    """
    site = urllib.urlopen(url)
    if site.getcode() == 404:
        deadLinks.append(url)

    # Check if the site has a fancy 404 page, i.e. no status code
    elif url.endswith('/404/'):
        deadLinks.append(url)
    elif '404' in url:
        # TODO: Make this a RE for the last /xxx/ or /xxx
        # Likely to produce many false positives
        deadLinks.append(url)
    else:
        happyLinks.append(url)

    return happyLinks, deadLinks

def spider(url, depth, maxDepth, urlDict):
    """
    :description: spider finds links and adds them to urlDict
    :return: urlDict
    """
    if depth >= maxDepth:
        return urlDict
    else:
        currentSite = urllib2.urlopen(url).read()
        soup = BeautifulSoup(currentSite)
        for link in soup.findAll('a'):
            dictEntry = str(link.get('href'))
            if dictEntry.startswith("http"):
                urlDict.update({dictEntry: "Not Visited"})
            elif dictEntry.startswith('/'): # e.g. /images
                if dictEntry.endswith('/'): # e.g. .com/
                    tmp = url + dictEntry[1:]
                else:
                    tmp = url + dictEntry
                urlDict.update({tmp: "Not Visited"})

        depth += 1
        return urlDict

def consolePrint(startingUrl, happyLinks, deadLinks, deadOnly):
    """
    Prints the output to the console or to a file
    if directed via >
    """

    if deadOnly == True:
        print "Dead Links: "
        for dead in deadLinks:
            print dead
    else:
        print "Dead Links: "
        for dead in deadLinks:
            print dead

        print "\nHappy Links"
        for happy in happyLinks:
            print happy

def main():
    startingUrl = sys.argv[1]; maxDepth = sys.argv[2]
    if sys.argv[3] == '-T':
        deadOnly = True
    else:
        deadOnly = False

    if sys.stdout.isatty():
        # Running in terminal, print reassuring message
        print "Finding dead links for: {}\n".format(startingUrl)
        print "You can create a file of dead links by $python 404.py {} 1 T > 404.txt\n".format(
            startingUrl)

    depth = 0
    urlDict = {}
    urlDict = spider(startingUrl, depth, maxDepth, urlDict)         # Starts spider
    deadLinks = []; happyLinks = []


    # Determine whether the url is valid or not
    for url in urlDict:
        happyLinks, deadLinks = returnCode(url, happyLinks, deadLinks)

    consolePrint(startingUrl, happyLinks, deadLinks, deadOnly)

if __name__ == '__main__':
    main()
