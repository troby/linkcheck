#!/usr/local/bin/python3.4
import linkcheck

lc=linkcheck.SiteChecker('google.com')
lc.check_site()
print('%s: %s' % (lc.sitename, lc.last_status))
