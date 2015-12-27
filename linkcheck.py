#!/usr/local/bin/python3.4
import requests, re, bs4

class SiteChecker:
  '''
    Tool for checking links of a site.
    Invoke with check = SiteChecker('mysite.com').
    self.sitename:      string containing base url of site to check
    self.visited:       list of urls already visited
    self.missing:       list of urls resulting in 404 response
    self.pruned:        list of prepared uris for testing
    self.last_status:   status code of most recent request
    self.last_encoding: encoding of most recent request
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
    self.visited = [self.sitename]
    self.missing = []
    self.pruned  = []

  def prune_uris(self, list):
    '''
      Take a list of anchor href links and cleanup as follows:
        * remove duplicates
        * convert relative paths to absolute URIs
        * forget about non-HTTP URI paths - like javascript:void()
        * remove any links found in self.visited
    '''
    for url in list:
      if url not in self.pruned:
        self.pruned.append(url)
    if self.sitename in self.pruned:
      self.pruned.remove(self.sitename)
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
    for url in self.pruned:
      if url in self.visited:
        self.pruned.remove(url)

  def check_site(self):
    '''
      Create request for self.sitename and handle response. Compile
      raw list of scraped links and run them through prune_uris().
    '''
    try:
      r=requests.get(self.sitename)
      self.last_status = r.status_code
      self.last_encoding = r.encoding
      if r.status_code != 200:
        print('%s error: %s' % (self.sitename, str(r.status_code)))
        return 1
    except:
      print('request failed: %s' % self.sitename)
      return 1

    bs = bs4.BeautifulSoup(r.text, 'html.parser')
    list = []
    for url in bs.find_all('a'):
      list.append(url.get('href'))
    self.prune_uris(list)

### TODO ###
# get all anchors
# find hrefs
# crawl urls for more urls
# remove previously visited urls
# verify external links exist, but do not crawl those pages
