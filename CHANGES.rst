CHANGELOG
=========

0.17.0
------

Date: 2017-01-19

- FIX: again some critical fixes in consul backend (don't use v0.16)
- FIX: cleanup ID now includes rancher environment name (rancher.sh change)
- FEATURE: contrib/congler helper added, script to delete and list services


0.16.0
------

Date: 2017-01-19

- FIX: small internal bug fix which should never have triggered
- CHANGE: cleanup ID now different, removal of standard "rancon" tag
- CHANGE: output of rancher.sh a bit different
- CHANGE: log outputs changed partially
- INTERNAL: some code refactorings


0.15.0
------

Date: 2017-01-19

- FEATURE: make consul urls dynamic (use %HOST% etc. placeholders)
- FEATURE: deregistering uses the correct consul instances, not blindly "the ones registered with"


0.14.0
------

Date: 2017-01-06

- FEATURE: add metric "rancon_registration_exceptions"


0.13.0
------

Date: 2017-01-05

- Very confused version. Maybe it's 0.14.0 already? Don't use.


0.12.0
------

Date: 2017-01-04

- FEATURE: add version number to '/' URL path & prometheus metrics


0.11.1
------

Date: 2017-01-04

- FIX: rancher.sh startup script processes env names with spaces now


0.11.0
------

Date: 2017-01-03

- FIX: Service tag replacment exception


0.10.0
------

Date: 2017-01-03

- FEATURE: Add "web interface" (basically only for metrics and health check)
- FEATURE: Add health check under /health
- FEATURE: Add prometheus metrics under /metrics
- CHANGE: Deregistration behavior for services which failed registration (was:
  unregister, is now: keep)


0.9.0
-----

Date: 2016-06-15

- CHANGE: convert IDs, tags, names to all lowercase in consul
- CHANGE: do not allow non-url characters in service IDs (basically nothing but [a-z0-9-])


0.8.0
-----

Date: 2016-06-15

- BREAKING: ``-i/--id`` parameter no longer global, moved to ``cleanup_id`` parameter of backend
- CHANGE: output now logging based, so all to stderr, and -vvvv flags possible
- FIX: bug in service lookup in Rancher
- OPEN: https connections


0.7.0
-----

Date: 2016-06-15

- FEATURE: authentication now used
- FIX: bug in service lookup in Rancher
- OPEN: https connections (untested, *might* work)


0.6.1
-----

Date: 2016-06-09

- More verbosity during init process


0.6.0
-----

Date: 2016-06-09

- Unified naming scheme of used environment variables
- Added convenience script "rancon.py"
- Dockerfile fixes
- Doc fixes


0.5.0
-----

Date: 2016-06-07

- Initial PyPI release
- module works, docker setup not tested yet
- documentation unfinished / not present
