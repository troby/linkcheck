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
