#!/usr/local/bin/python3.4
import requests, re, bs4

# globals
class SiteChecker:
  '''
    Tool for checking links of a site.
    Invoke with check = SiteChecker('http://mysite.com')
    self.url:     string containing base url of site to check
    self.visited: list of urls already visited
    self.missing: list of urls resulting in 404 response
    self.pruned:  list of prepared uris for testing
  '''

  def __init__(self, url):
    if not re.match(r'^http(s)?://.*', url):
      url = 'http://' + url
    if not re.match(r'.*/$', url):
      url = url + '/'
    self.url = url

  visited = []
  missing = []
  pruned  = []

  # clean url list
  def prune_uris(self, list):
    for url in list:
      if url not in self.pruned:
        self.pruned.append(url)
    list = self.pruned
    self.pruned = []
    for url in list:
      if ':' not in url:
        url = re.sub('^/+', '', url)
        url = self.url + url
        self.pruned.append(url)
        continue
      if ':' in url:
        if ('http://' in url) or ('https://' in url):
          self.pruned.append(url)

# request page
# get all anchors
# find hrefs
# clean urls
# save urls
# crawl urls for more urls
# remove previously visited urls
# track 404s
