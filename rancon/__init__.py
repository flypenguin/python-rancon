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
    backend = settings.backend
    source = settings.source
    routed_services = source.get_services()
    registered_services = []
    for service in routed_services:
        rv = backend.register(service)
        if rv:
            registered_services.append(rv)
        else:
            print("Failed to register service: {}"
                  .format(service))
    backend.cleanup(registered_services)


def start(sys_argv):
    # prepare
    settings.parse_params(sys_argv)
    # run
    print("RANCON: start @ {}".format(ctime()))
    print("RANCON: CLEANUP ID: {}".format(settings.args.id))
    route_services()
    while settings.args.continuous:
        sleep(settings.args.wait)
        route_services()
    print("RANCON: Done.")


def console_entrypoint():
    start(sys.argv[1:])
