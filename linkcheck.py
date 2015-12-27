#!/usr/local/bin/python3.4
import requests, re, bs4

class SiteChecker:
  '''
    Tool for checking links of a site.
    Invoke with check = SiteChecker('mysite.com').
    self.sitename:      string containing submitted site to check
    self.base_url:      string containing base url of site
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
    if not (re.match(r'.*/$', url)) and not (re.match(r'.*(htm|html)$', url)):
      url = url + '/'
    self.sitename = url
    self.base_url = re.sub(r'^([htps]+://[^/]+/).*', '\\1', url)
    tmp = re.sub(r'^(.*)/$', '\\1', self.base_url)
    self.encodings = ['ISO-8859-1', 'UTF-8']
    self.visited = [self.sitename, tmp, self.base_url]
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

  def scrape_url(self, url):
    '''
      Create request for self.sitename and handle response. Compile
      raw list of scraped links and run them through prune_uris().
    '''
    try:
      r=requests.get(url)
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
    return 0

  def test_link(self, url):
    '''
      Check link.
      Handle response.
      If known text encoding scrape for more links.
      Add link to visited and status dict.
    '''

### TODO ###
# crawl urls for more urls
# remove previously visited urls
# verify external links exist, but do not crawl those pages
# use encoding to differentiate between downloads and pages
# verify downloads but do not fetch them
