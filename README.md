# Rancon

(expect the name to change ... it's stupid)

Takes information from currently rancher and forwards it into a service registry (currently consul). This information is - for me at least - intended to be used to configure a load balancer for dynamic traffic routing.

Documentation is pretty incomplete, but might be self-explanatory if called.

    python -m rancon --help


## Super quick start

- clone rancon
- add a service in rancher
    - assign a label `rancon.routing` with the value of `true`
- start rancon `python -m rancon rancher consul -s url=rancherurl -b url=consulurl`
- look at the output


## State

WORKING:

- discovery

NONWORKING:

- actually add entries in consul
- rancher with authentication
- consul with TLS

PLANNED:

- traefik support
- maybe a more generic approach, cause this forwarding thing might be useful for more than just load balancing

