#!/usr/local/bin/python3.4
import linkcheck, sys

list = [
  'http://site.com/link.html',
  'http://site.com/site.html',
  'https://site.com/index.html',
  'http://site.com/link.html',
  'static.html',
  '/about.html',
  'javascript:void(0)',
  'http://mysite.com/',
]

# class initialization
try:
  mysite = linkcheck.SiteChecker('mysite.com')
  assert mysite.sitename == 'http://mysite.com/'
  assert mysite.base_url == 'http://mysite.com/'
  assert mysite.visited == ['http://mysite.com/','http://mysite.com','http://mysite.com/']
  assert mysite.missing == []
  assert mysite.pruned == []
  print('class initialization OK')
except:
  print('class initialization FAIL')
  sys.exit(1)

# test uri pruning
try:
  mysite.prune_uris(list)
  assert len(mysite.pruned) == 5
  assert 'http://site.com/link.html' in mysite.pruned
  assert 'http://site.com/site.html' in mysite.pruned
  assert 'https://site.com/index.html' in mysite.pruned
  assert 'http://mysite.com/static.html' in mysite.pruned
  assert 'http://mysite.com/about.html' in mysite.pruned
  print('prune_uris() OK')
except:
  print('prune_uris() FAIL')

# test removal of visited links
try:
  mysite.visited.append('http://mysite.com/visited.html')
  mysite.pruned = []
  list.append('http://mysite.com/visited.html')
  mysite.prune_uris(list)
  assert len(mysite.pruned) == 5
  assert 'http://mysite.com/visited.html' not in mysite.pruned
  print('remove visited OK')
  list.remove('http://mysite.com/visited.html')
except:
  print('remove visited FAIL')

# test sitename with html path
try:
  del mysite
  mysite = linkcheck.SiteChecker('mysite.com/index.html')
  assert mysite.sitename == 'http://mysite.com/index.html'
  assert mysite.base_url == 'http://mysite.com/'
  mysite.prune_uris(list)
  assert len(mysite.pruned) == 5
  assert 'http://site.com/link.html' in mysite.pruned
  assert 'http://site.com/site.html' in mysite.pruned
  assert 'https://site.com/index.html' in mysite.pruned
  assert 'http://mysite.com/static.html' in mysite.pruned
  assert 'http://mysite.com/about.html' in mysite.pruned
  print('set self.domain OK')
except:
  print('set self.domain FAIL')
