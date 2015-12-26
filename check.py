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
  '''
  def __init__(self, url):
    self.url = url
  visited = []
  missing = []

# request page
# get all anchors
# find hrefs
# clean urls
# save urls
# crawl urls for more urls
# remove previously visited urls
# track 404s

# clean url list
# remove duplicates
def remove_duplicates(list):
  new_list=[]
  for url in list:
    if url not in new_list:
      new_list.append(url)
  return new_list
# remove non-http URIs
def remove_nonhttp_uri(list):
  new_list=[]
  for url in list:
    if ':' not in url:
      new_list.append(url)
      continue
    if ':' in url:
      if ('http://' in url) or ('https://' in url):
        new_list.append(url)
  return new_list
