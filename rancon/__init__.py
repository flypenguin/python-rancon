"""
Crawl through all available rancher services and look for a label with
the following format:

    rancon.routing: true / on / yes / 1

If a service with this tag is found, it will be published as service
"SERVICE_NAME" in Consul, and the service will get the tag TAG_NAME (if
set).

If "rancon.consul.tag" is not found, the tag "rancher_service" is used.
The tag "rancon" is applied every time.

*All* services created by rancon will be tagged "rancon" in consul, so that
rancon is able to remove services which are no longer available in rancher.

"""

from rancon import settings

from cattleprod import poke

import sys
from collections import defaultdict


def get_previously_created_consul_services():
    return []


def get_routable_services():
    starting_point = poke(settings.args.rancher_url)
    rv = defaultdict(list)
    for env in starting_point.get_environments():
        for service in env.get_services():
            if "rancon.routing" in service.data.fields.launchConfig.labels:
                rv[env.name].append(service)
    return rv


def route_services():
    existing_service_ids = get_previously_created_consul_services()
    envs_services = get_routable_services()

    for env, services in envs_services.items():
        for srv in services:
            print("Found routable service %s.%s" % (srv.name, env))


def start(sys_argv):
    settings.parse_params(sys_argv)
    #while True:
    route_services()


def console_entrypoint():
    start(sys.argv[1:])
