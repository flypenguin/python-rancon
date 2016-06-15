"""
Crawls through the 'source' source and looks for labels starting with 'rancon'.

If such a label is found on a service, then it will register the service in the
'backend'. If the backend supports tag all services will be tagged 'rancon'.
depending on the backend the registration behavior can be influenced by tags
set on the source (e.g. rancon.name, ...).

Every rancon.* tag will be available as variable "%NAME%" in the backend.
Please look through the documentation to make more sense of this, it is easy
but just a little bit complex because of the flexibility.
"""

from rancon import settings
from rancon import tools

import sys
from time import sleep, ctime


def route_services():
    log = tools.getLogger(__name__)
    backend = settings.backend
    source = settings.source
    routed_services = source.get_services()
    registered_services = []
    for service in routed_services:
        rv = backend.register(service)
        if rv:
            registered_services.append(rv)
        else:
            log.warn("Failed to register service: {}"
                     .format(service))
    if len(registered_services) == 0:
        log.warn("No services registered (of {} services found)"
                 .format(len(registered_services), len(routed_services)))
    backend.cleanup(registered_services)
    log.warn("Run completed @ {}".format(ctime()))


def start(sys_argv):
    # prepare
    settings.parse_params(sys_argv)
    # not before here :)
    log = tools.getLogger(__name__)
    # run
    log.error("Start @ {}".format(ctime()))
    route_services()
    while settings.args.continuous:
        sleep(settings.args.wait)
        route_services()
    log.info("Exiting.")


def console_entrypoint():
    start(sys.argv[1:])
