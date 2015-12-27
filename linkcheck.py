#!/usr/local/bin/python3.4
import requests, re, bs4

class SiteChecker:
  '''
    Tool for checking links of a site.

    Usage:
      check = linkcheck.SiteChecker('mysite.com')
      check.start()

    self.sitename:      string containing submitted site to check
    self.base_url:      string containing base url of site
    self.visited:       list of urls already visited
    self.missing:       list of urls resulting in 404 response
    self.pruned:        list of prepared uris for testing
    self.last_status:   status code of most recent request
    self.last_encoding: encoding of most recent request
    self.verbose:	set to True for more information
  '''

  def __init__(self, url):
    '''
      Provide url for testing.
      If a lazy name (like google.com) is provided,
      prepend http:// and append backslash.
    '''
    if not re.match(r'^http(s)?://.*', url):
      url = 'http://' + url
    if not (re.match(r'.*/$', url)) and not (re.match(r'.*(htm|html)$', url)):
      url = url + '/'
    self.sitename = url
    self.base_url = re.sub(r'^([htps]+://[^/]+/).*', '\\1', url)
    tmp = re.sub(r'^(.*)/$', '\\1', self.base_url)
    self.encodings = ['ISO-8859-1', 'UTF-8']
    self.visited = [self.sitename, tmp, self.base_url]
    self.missing = []
    self.pruned  = []
    self.verbose = False

  def start(self):
    return self.check_url(self.sitename)

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
      Create request for self.sitename and handle response.
      Pass off to scrape_url if valid encoding.
    '''
    try:
      if self.verbose:
        print('trying %s' % url)
      r=requests.get(url, stream=True)
      self.last_status = r.status_code
      self.last_encoding = r.encoding
      if (r.status_code != 200) and (r.status_code != 404):
        print('%s error: %s' % (url, str(r.status_code)))
        return False
    except:
      r.close()
      return False
    if url != self.sitename:
      self.visited.append(url)
    if self.last_status == 404:
      self.missing.append(url)
      r.close()
      return True
    if (self.last_encoding.upper() in self.encodings) and (self.is_local(url)):
      rv = self.scrape_url(r.text)
      r.close()
      return rv

  def scrape_url(self, links):
    '''
      Compile raw list of scraped links and run them through prune_uris().
    '''
    bs = bs4.BeautifulSoup(links, 'html.parser')
    list = []
    for url in bs.find_all('a'):
      list.append(url.get('href'))
    self.prune_uris(list)
    return True

### TODO ###
# crawl urls for more urls
# remove previously visited urls
# verify external links exist, but do not crawl those pages
# use encoding to differentiate between downloads and pages
# verify downloads but do not fetch them
