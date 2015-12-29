#!/usr/bin/env python3
import linkcheck, sys, io

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

total = 0
success = 0

# class initialization
total += 1
try:
  mysite = linkcheck.SiteChecker('mysite.com/path.html')
  assert mysite.sitename == 'http://mysite.com/path.html'
  assert mysite.base_url == 'http://mysite.com/'
  assert mysite.visited == ['http://mysite.com/path.html','http://mysite.com', 'http://mysite.com/']
  del mysite

  mysite = linkcheck.SiteChecker('mysite.com')
  assert mysite.sitename == 'http://mysite.com/'
  assert mysite.base_url == 'http://mysite.com/'
  assert mysite.visited == ['http://mysite.com/','http://mysite.com']
  assert mysite.missing == []
  assert mysite.pruned == []
  print('class initialization OK')
  success += 1
except:
  print('class initialization FAIL')
  sys.exit(1)

# test uri pruning
total += 1
try:
  mysite.prune_uris(list)
  assert len(mysite.pruned) == 5
  assert 'http://site.com/link.html' in mysite.pruned
  assert 'http://site.com/site.html' in mysite.pruned
  assert 'https://site.com/index.html' in mysite.pruned
  assert 'http://mysite.com/static.html' in mysite.pruned
  assert 'http://mysite.com/about.html' in mysite.pruned
  print('prune_uris() OK')
  success += 1
except:
  print('prune_uris() FAIL')

# test removal of visited links
total += 1
try:
  mysite.visited.append('http://mysite.com/visited.html')
  mysite.pruned = []
  list.append('http://mysite.com/visited.html')
  mysite.prune_uris(list)
  assert len(mysite.pruned) == 5
  assert 'http://mysite.com/visited.html' not in mysite.pruned
  print('remove visited OK')
  list.remove('http://mysite.com/visited.html')
  success += 1
except:
  if 'http://mysite.com/visited.html' in list:
    list.remove('http://mysite.com/visited.html')
  print('remove visited FAIL')

# test sitename with html path
total += 1
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
  print('test html path OK')
  success += 1
except:
  print('test html path FAIL')

# test is_local()
total += 1
try:
  assert mysite.is_local('http://site.com/link.html') is False
  assert mysite.is_local('http://site.com/site.html') is False
  assert mysite.is_local('https://site.com/index.html') is False
  assert mysite.is_local('http://mysite.com/static.html') is True
  assert mysite.is_local('http://mysite.com/about.html') is True
  print('test is_local() OK')
  success += 1
except:
  print('test is_local() FAIL')

# test results()
total += 1
try:
  del mysite
  mysite = linkcheck.SiteChecker('mysite.com')
  mysite.missing.append('http://mysite.com/missing.html')
  mysite.missing.append('http://mysite.com/another.html')
  expected_results = \
    'missing links:\n' + \
    mysite.missing[0] + '\n' + \
    mysite.missing[1] + '\n'

  cap_output=io.StringIO()
  default_output=sys.stdout
  sys.stdout=cap_output
  mysite.results()
  assert cap_output.getvalue() == expected_results
  sys.stdout=default_output
  print('results() output OK')
  success += 1
except:
  sys.stdout=default_output
  print('results() output FAIL')

print('%d of %d tests successful.' % (success, total))
