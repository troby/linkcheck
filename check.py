#!/usr/local/bin/python3.4
import requests, re, bs4

class SiteChecker:
  '''
    Tool for checking links of a site.
    Invoke with check = SiteChecker('mysite.com')
    self.sitename:     string containing base url of site to check
    self.visited:      list of urls already visited
    self.missing:      list of urls resulting in 404 response
    self.pruned:       list of prepared uris for testing
  '''

  def __init__(self, url):
    '''
      Provide url for testing.
      If a lazy name (like google.com) is provided,
      prepend http:// and append backslash.
    '''
    if not re.match(r'^http(s)?://.*', url):
      url = 'http://' + url
    if not re.match(r'.*/$', url):
      url = url + '/'
    self.sitename = url

  visited = []
  missing = []
  pruned  = []

  def prune_uris(self, list):
    '''
      take a list of anchor href links and cleanup as follows:
        * remove duplicates
        * convert relative paths to absolute URIs
        * forget about non-HTTP URI paths - like javascript:void()
    '''
    for url in list:
      if url not in self.pruned:
        self.pruned.append(url)
    list = self.pruned
    self.pruned = []
    for url in list:
      if ':' not in url:
        url = re.sub('^/+', '', url)
        url = self.sitename + url
        self.pruned.append(url)
        continue
      if ':' in url:
        if ('http://' in url) or ('https://' in url):
          self.pruned.append(url)

### TODO ###
# request page
# get all anchors
# find hrefs
# crawl urls for more urls
# remove previously visited urls
# verify external links exist, but do not crawl those pages
# remove reoccurances of sitename
