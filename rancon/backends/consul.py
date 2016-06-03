from . import BackendBase

import consul

from pprint import pformat
from urllib.parse import urlparse as up


class ConsulBackend(BackendBase):

    required_opts = ('url',)

    def __init__(self, url):
        print("CONSUL: INIT: with url {}".format(url))
        parsed_url = up(url)
        items = parsed_url.netloc.split(":")
        if len(items) == 1:
            self.consul = consul.Consul(host=parsed_url.netloc,
                                        scheme=parsed_url.scheme)
        else:
            self.consul = consul.Consul(host=items[0], port=items[1],
                                        scheme=parsed_url.scheme)

    def register(self, service):
        print("CONSUL: ADD_SERVICE: service '{}' on '{}:{}'"
              .format(service.name, service.host, service.port))
        print("CONSUL: ADD_SERVICE: further args: {}"
              .format(pformat(service.other)))

    def cleanup(self, marker):
        print("CONSUL: CLEANUP: called with '{}'".format(marker))


def get():
    return ConsulBackend
