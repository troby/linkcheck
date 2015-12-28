#!/usr/local/bin/python3.4
import linkcheck

lc=linkcheck.SiteChecker('127.0.0.1')
lc.start()
assert lc.last_status == 200
assert len(lc.pruned) == 2
assert 'http://127.0.0.1/download.html' in lc.pruned
assert 'http://127.0.0.1/missing_1.html' in lc.pruned
