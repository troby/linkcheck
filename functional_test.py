#!/usr/local/bin/python3.4
import linkcheck

lc=linkcheck.SiteChecker('127.0.0.1')
lc.verbose=True
lc.delay=0
lc.start()
lc.results()
assert len(lc.visited) == 6
assert len(lc.missing) == 2
assert len(lc.pruned) == 0
assert 'http://127.0.0.1/missing_1.html' in lc.missing
assert 'http://127.0.0.1/missing_2.html' in lc.missing
