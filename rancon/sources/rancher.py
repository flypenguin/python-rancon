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

    def get_services(self):
        starting_point = poke(self.url)
        rv = []
        for service in starting_point.get_services():
            if "rancon.routing" in service.data.fields.launchConfig.labels:
                endpoints = service.data.fields.publicEndpoints
                if len(endpoints) > 1:
                    print("WARNING: more than one endpoint for service {},\n"
                          "         don't know what to do."
                          .format(service.name))
                elif len(endpoints) == 0:
                    print(
                        "WARNING: no public endpoints for service '{}', ignoring."
                        .format(service.name))
                else:
                    host = endpoints[0]['ipAddress']
                    port = endpoints[0]['port']
                    rv.append(Service(name=service.name,
                                      host=host, port=port, source=service))
        return rv


def get():
    return RancherSource
