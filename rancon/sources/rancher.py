from . import SourceBase
from rancon.service import Service

from cattleprod import poke


class RancherSource(SourceBase):

    required_opts = ('url',)
    additional_opts = ('accesskey', 'secretkey')

    def __init__(self, url, accesskey=None, secretkey=None):
        self.url = url
        self.access = accesskey
        self.secret = secretkey

    def get_services(self, **_):
        starting_point = poke(self.url)
        rv = []
        stacks = {}
        for service in starting_point.get_services():
            if "rancon.routing" in service.data.fields.launchConfig.labels:
                endpoints = service.data.fields.publicEndpoints
                if len(endpoints) > 1:
                    print("RANCHER: WARNING: > 1 endpoints for service '{}'. "
                          "Ignoring."
                          .format(service.name))
                elif len(endpoints) == 0:
                    print(
                        "RANCHER: WARNING: No public endpoints "
                        "for service '{}'. Ignoring."
                        .format(service.name))
                else:
                    host = endpoints[0]['ipAddress']
                    port = endpoints[0]['port']
                    stacks[service.links.environment] = None
                    rv.append(Service(name=service.name,
                                      host=host, port=port, source=service))
        # find names for the stacks in the services, limit rancher calls (one
        # for all services, one for each stack) instead of 2x per service
        for stack in stacks.keys():
            stack_service = poke(stack)
            stacks[stack] = stack_service.name
        for service in rv:
            service.meta['stack'] = stacks[service.source.links.environment]
        return rv


def get():
    return RancherSource
