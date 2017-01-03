from rancon.tools import tag_replace, getLogger
from . import BackendBase

import consul

from re import sub as resub
from urllib.parse import urlparse as up


_default_id_schema = '%NAME%_%HOST%_%PORT%'
_default_cleanup_id = 'default'
_default_consul_url = 'http://%HOST%:8500'


class ConsulBackend(BackendBase):

    additional_opts = ('url', 'id_schema', 'cleanup_id')

    # let's add a program command which displays this help text some time
    # later. might be really helpful not to have to look into code.
    opts_help = {
        'url': "The consul URL to use to register / deregister services. "
               "Default: '{}'"
               .format(_default_consul_url),
        'id_schema': 'Naming schema for services in consul. '
                     'Default: {}'
                     .format(_default_id_schema),
        'cleanup_id': "Rancon adds this tag to all services it registers, and "
                      "only deregisters services with the same tag set while "
                      "ignoring all others. Default: '{}'"
                      .format(_default_cleanup_id)
    }

    def __init__(self,
                 url=_default_consul_url,
                 id_schema=_default_id_schema,
                 cleanup_id=_default_cleanup_id):
        self.log = getLogger(__name__)
        self.url = url
        self.id_schema = id_schema
        self.cleanup_id = cleanup_id.lower()
        self.log.error("INIT: url={}".format(url))
        self.log.error("INIT: id_schema={}".format(self.id_schema))
        self.log.error("INIT: cleanup_id={}".format(self.cleanup_id))

    def configure(self, services):
        # lower everything, consul should not have upper/lower case distinction
        svc_id = self._get_service_id(services)
        svc_name = services.name.lower()
        con = self._get_consul_instance_for(services)
        success = con.agent.service.configure(
            svc_name,
            svc_id,
            address=services.host, port=int(services.port),
            tags=self._get_tags(services),
        )
        if success:
            self.log.warn("REGISTER: {} using {} / {} (cleanup id: {})"
                          .format(services, svc_name, svc_id,
                                  self._get_cleanup_tag()))
            return svc_id
        else:
            self.log.warn("REGISTER: FAILED registering "
                          "service {} using {} / {}"
                          .format(services, svc_name, svc_id))
            return None

    def cleanup(self, keep_services):
        check_tag = self._get_cleanup_tag()
        for svc_id, svc in con.agent.services().items():
            if not svc['Tags'] or check_tag not in svc['Tags']:
                continue
            if svc_id not in keep_services:
                self.log.warn("CLEANUP: de-registering service id {}"
                              .format(svc_id))
                con.agent.service.deregister(svc_id)

    def _get_consul_instance_for(self, service):
        url = tag_replace(self.url, service)
        parsed_url = up(url)
        items = parsed_url.netloc.split(":")
        # can be a list.
        if len(items) == 1:
            rv = consul.Consul(host=parsed_url.netloc,
                               scheme=parsed_url.scheme)
        else:
            rv = consul.Consul(host=items[0], port=items[1],
                               scheme=parsed_url.scheme)
        return rv

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
        return resub(r"[^a-z0-9-]", "-", tmp)


def get():
    return ConsulBackend
