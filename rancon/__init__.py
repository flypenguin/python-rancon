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

import sys
from time import sleep, ctime

from rancon import settings
from rancon import tools


def route_services():
    """ checks for services to register and then  """
    log = tools.getLogger(__name__)
    backend = settings.backend
    source = settings.source
    services_to_route = source.get_services()
    registered_services = []

    for service in services_to_route:
        routed_service = backend.register(service)
        if routed_service is None:
            log.warn("Failed to register service: {}".format(service))
        else:
            registered_services.append(routed_service)

    if len(registered_services) == 0:
        # To ABK: got rid of the warning [only one format {} was defined]
        # but don't know what you wanted to do here.
        log.warn("No services registered (of {} + {} services found)"
                 .format(len(registered_services), len(services_to_route)))
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
