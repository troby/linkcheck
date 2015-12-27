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
]

# class initialization
try:
  mysite = linkcheck.SiteChecker('mysite.com')
  assert mysite.sitename == 'http://mysite.com/'
  assert mysite.visited == []
  assert mysite.missing == []
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
