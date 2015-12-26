#!/usr/local/bin/python3.4
import check

list = [
  'http://site.com/link.html',
  'http://site.com/site.html',
  'https://site.com/index.html',
  'http://site.com/link.html',
  'static.html',
  'javascript:void(0)',
]

try:
  new = check.remove_duplicates(list)
  assert len(new) == 5
  assert 'http://site.com/link.html' in new
  assert 'http://site.com/site.html' in new
  assert 'https://site.com/index.html' in new
  assert 'javascript:void(0)' in new
  assert 'static.html' in new
  print('remove_duplicates() OK')
except:
  print('remove_duplicates() FAIL')

try:
  new = check.remove_nonhttp_uri(list)
  assert len(new) == 5
  assert 'http://site.com/link.html' in list
  assert 'http://site.com/site.html' in list
  assert 'https://site.com/index.html' in list
  assert 'http://site.com/link.html' in list
  assert 'static.html' in list
  print('remove_nonhttp_uri() OK')
except:
  print('remove_nonhttp_uri() FAIL')

try:
  mysite = check.SiteChecker('http://mysite.com/')
  assert mysite.url == 'http://mysite.com/'
  assert mysite.visited == []
  assert mysite.missing == []
  print('SiteChecker class OK')
except:
  print('SiteChecker class FAIL')
