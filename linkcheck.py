#!/usr/local/bin/python3.4
import requests, re, bs4, time

class SiteChecker:
  '''
    Tool for checking links of a site.

    Usage:
      check = linkcheck.SiteChecker('mysite.com')
      check.start()
      check.verbose = True
      check.delay = 20

    self.sitename:      string containing submitted site to check
    self.base_url:      string containing base url of site
    self.visited:       list of urls already visited
    self.missing:       list of urls resulting in 404 response
    self.pruned:        list of prepared uris for testing
    self.last_status:   status code of last response
    self.last_encoding: encoding of last response
    self.last_text:     text of last response or None
    self.verbose:	set to True for more information
    self.delay:         delay in seconds between each request (default 3)
  '''

  def __init__(self, url):
    '''
      Provide url for testing.
      If a lazy name (like google.com) is provided,
      prepend http:// and append backslash.
    '''
    if not re.match(r'^http(s)?://.*', url):
      url = 'http://' + url
    if not (re.match(r'.*/$', url)) and not (re.match(r'.*(htm|html|php)$', url)):
      url = url + '/'
    self.sitename = url
    self.base_url = re.sub(r'^([htps]+://[^/]+/).*', '\\1', url)
    tmp = re.sub(r'^(.*)/$', '\\1', self.base_url)
    self.encodings = ['ISO-8859-1', 'UTF-8']
    self.visited = [self.sitename, tmp]
    if self.sitename != self.base_url:
      self.visited.append(self.base_url)
    self.missing = []
    self.pruned  = []
    self.verbose = False
    self.delay = 3

  def start(self):
    if self.check_url(self.sitename):
      self.scrape_hrefs()
    while len(self.pruned) > 0:
      time.sleep(self.delay)
      if self.check_url(self.pruned[0]):
        self.scrape_hrefs()

  def prune_uris(self, list):
    '''
      Take a list of anchor href links and cleanup as follows:
        * remove duplicates
        * convert relative paths to absolute URIs
        * forget about non-HTTP URI paths - like javascript:void()
        * remove any links found in self.visited
    '''
    for url in list:
      if (url not in self.pruned) and (url not in self.visited):
        self.pruned.append(url)

    for url in self.pruned:
      if ':' not in url:
        index = self.pruned.index(url)
        trimmed = re.sub('^/+', '', url)
        self.pruned[index] = self.base_url + trimmed
      else:
        if ('http://' not in url) and ('https://' not in url):
          self.pruned.remove(url)

  def is_local(self, url):
    '''
      Test if url is part of base site being tested.
    '''
    if self.base_url in url:
      return True
    else:
      return False

  def check_url(self, url):
    '''
      Create request for url and handle response.
      Pass off to scrape_hrefs if valid encoding.
      Return boolean result.
    '''
    self.last_status = None
    self.last_encoding = None
    self.last_text = None
    if self.verbose:
      print('trying %s' % url)
    try:
      r=requests.get(url, stream=True)
      self.last_status = r.status_code
      self.last_encoding = r.encoding
      if r.encoding and (self.is_local(url)):
        if r.encoding.upper() in self.encodings:
          self.last_text = r.text
        else:
          print('unknown encoding: %s' % r.encoding)
      r.close()
    except:
      r.close()
      return False

    if self.verbose:
      print('response: %s' % r.status_code)
    if self.verbose:
      print('encoding: %s' % r.encoding)

    if url in self.pruned:
      self.pruned.remove(url)
    if url not in self.visited:
      self.visited.append(url)

    if r.status_code == 404:
      if self.verbose:
        print('add to missing: %s' % url)
      self.missing.append(url)

    if (r.status_code == 200) and (self.last_text):
      return True
    else:
      return False

  def scrape_hrefs(self):
    '''
      Compile raw list of scraped links and run them through prune_uris().
    '''
    bs = bs4.BeautifulSoup(self.last_text, 'html.parser')
    list = []
    for url in bs.find_all('a'):
      list.append(url.get('href'))
    self.prune_uris(list)

### TODO ###
# crawl urls for more urls
# remove previously visited urls
