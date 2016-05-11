Rancon (aka rancher-consul)
===========================

We use consul as a service discovery mechanism, and a Consul-template / HAProxy combination to route traffic into our services. This python script is a helper to automatically enter Rancher services into Consul based on Rancher label selectors, so they can picked up by the load HAProxy load balancing layer.

This might not be of any use to anybody but me, but I'll make it public anyway because I did not find another solution so I had to write it, and maybe someone else has the same problem.
