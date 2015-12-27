#!/usr/local/bin/python3.4
import linkcheck

lc=linkcheck.SiteChecker('google.com')
if lc.start():
  print('%s: %s' % (lc.sitename, lc.last_status))
  print('encoding: %s' % lc.last_encoding)
  import pprint
  pprint.pprint(lc.pruned)
else:
  print('scrape failed: %s' % lc.sitename)
