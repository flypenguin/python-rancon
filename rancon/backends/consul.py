""" Module containing the backend implementation for consul """

import re
import urllib.parse
import time

import consul
import prometheus_client.core

from rancon.tools import tag_replace, getLogger
from . import BackendBase


class ConsulBackend(BackendBase):
    """ Implementation of consul backend """

    required_opts = ('url',)
    additional_opts = ('id_schema', 'cleanup_id')

    def __init__(self, url,
                 id_schema='%NAME%_%HOST%_%PORT%',
                 cleanup_id='default'):
        self.log = getLogger(__name__)

        self.id_schema = id_schema
        self.cleanup_id = cleanup_id.lower()

        parsed_url = urllib.parse.urlparse(url)

        # port specified?
        if ":" in parsed_url.netloc:
            host, port = parsed_url.netloc.split(":")
            self.consul = consul.Consul(host=host, port=port,
                                        scheme=parsed_url.scheme)
        else:
            self.consul = consul.Consul(host=parsed_url.netloc,
                                        scheme=parsed_url.scheme)

        self.log.info("CONSUL INIT: url={}".format(url))
        self.log.info("CONSUL INIT: id_schema={}".format(self.id_schema))
        self.log.info("CONSUL INIT: cleanup_id={}".format(self.cleanup_id))
        self.register_service_summary = prometheus_client.core.Summary('rancon_register_service_seconds', 'Number of seconds register_service takes')

    def register(self, service):
        """Register the service in consul.
        :return: (BOOL(success), STR(svc_id))
        """
        start = time.time()
        # lower everything, consul should not have upper/lower case distinction
        svc_id = self._get_service_id(service)
        svc_name = service.name.lower()

        success = self.consul.agent.service.register(
            svc_name,
            svc_id,
            address=service.host, port=int(service.port),
            tags=self._get_tags(service),
        )
        self.register_service_summary.observe(time.time() - start)

        if success:
            self.log.info("REGISTER: {} using {} / {} (cleanup id: {})"
                          .format(service, svc_name, svc_id,
                                  self._get_cleanup_tag()))
        else:
            self.log.warn("REGISTER: FAILED registering "
                          "service {} using {} / {}"
                          .format(service, svc_name, svc_id))
        return success, svc_id

    def cleanup(self, keep_services):
        con = self.consul
        check_tag = self._get_cleanup_tag()
        for svc_id, svc in con.agent.services().items():
            if not svc['Tags'] or check_tag not in svc['Tags']:
                continue
            if svc_id not in keep_services:
                self.log.warn("CLEANUP: de-registering service id {}"
                              .format(svc_id))
                con.agent.service.deregister(svc_id)

    def _get_tags(self, service):
        tag_list_str = service.get('tag', '')
        tag_list = tag_list_str.split(",") if tag_list_str else []
        return [tag_replace(x, service).strip().lower() for x in tag_list] + \
               [self._get_cleanup_tag(),
                'rancon']

    def _get_cleanup_tag(self):
        return "rancon-cleanup-id-{}".format(self.cleanup_id)

    def _get_service_id(self, service):
        tmp = tag_replace(self.id_schema, service).lower()
        return re.sub(r"[^a-z0-9-]", "-", tmp)


def get():
    """ returns this model's main class """
    return ConsulBackend
