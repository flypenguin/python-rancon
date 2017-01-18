""" Module containing the backend implementation for consul """

import re
import urllib.parse
import time

import consul
import prometheus_client.core
from dotmap import DotMap

from rancon.tools import tag_replace, getLogger
from . import BackendBase


_URL_DEFAULT = 'http://%HOST%:8500'

PROM_REGISTER_SERVICE_TIME = prometheus_client.core.Summary(
    'rancon_register_service_seconds',
    'Number of seconds register_service takes')


class ConsulBackend(BackendBase):
    """ Implementation of consul backend """

    required_opts = ()
    additional_opts = ('url', 'id_schema', 'cleanup_id')

    def __init__(self,
                 url=_URL_DEFAULT,
                 id_schema='%NAME%_%HOST%_%PORT%',
                 cleanup_id='default'):
        self.log = getLogger(__name__)
        # instance vars
        self.consul_url = url
        self.id_schema = id_schema
        self.cleanup_id = cleanup_id.lower()
        # consul instance cache
        self.consul_inst_cache = {}
        # log output
        self.log.info("CONSUL INIT: url={}".format(url))
        self.log.info("CONSUL INIT: id_schema={}".format(self.id_schema))
        self.log.info("CONSUL INIT: cleanup_id={}".format(self.cleanup_id))
        # no consul instance here now, cause we need to allow for dynamic
        # URLs (http://%HOST%:1234)

    def _get_consul_for(self, service) -> consul.Consul:
        # no replacments -> always the same cache_str :)
        consul_url = tag_replace(self.consul_url, service)
        if consul_url not in self.consul_inst_cache:
            # extract host and port separately, just for the constructor call
            # of consul.Consul()
            parsed_url = urllib.parse.urlparse(consul_url)
            port = 8500             # default from consul.Consul
            host = parsed_url.netloc
            if ":" in parsed_url.netloc:            # port specified?
                items = host.split(":")             # extract and use
                host, port = (items[0], int(items[1]))
            # create consul instance and put in cache
            self.consul_inst_cache[consul_url] = \
                consul.Consul(host=host, port=port, scheme=parsed_url.scheme)
        return self.consul_inst_cache[consul_url]

    def register(self, service) -> (bool, str):
        """Register the service in consul.
        :return: (BOOL(success), STR(svc_id))
        """
        con = self._get_consul_for(service)
        # lower everything, consul should not have upper/lower case distinction
        svc_id = self._get_service_id(service)
        svc_name = service.name.lower()

        start = time.time()
        success = con.agent.service.register(
            svc_name,
            svc_id,
            address=service.host, port=int(service.port),
            tags=self._get_tags(service),
        )
        PROM_REGISTER_SERVICE_TIME.observe(time.time() - start)

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
        """
        Starts the cleanup procedure, which is basically get all services
        and remove all which fit the following criteria:
        * have the check_tag of rancon set
        * their id is not in the list of the keep_services parameter
        :param keep_services: A list of service ids [id1, id2, ...]
        :return: None
        """
        if len(self.consul_inst_cache) == 0:
            # no services registered, so we don't have any consul instance.
            # if we dont have one, just return (cause we can't connect to
            # anything, right?)
            return

        # take any consul instance to get the service list, py3 style
        con = next(iter(self.consul_inst_cache.values()))
        check_tag = self._get_cleanup_tag()

        # one call to consul. returns (INDX, {SVC_NAME:[SVC_TAGS,...], ...})
        # so we want only the dict: {SVC_NAME: SVC_TAGS, ...}
        _tmp = con.catalog.services()[1]
        chk_svc_names = [
            svc_name for svc_name, svc_tags in _tmp.items()
            if check_tag in svc_tags
        ]

        # a LOT of calls to consul (we don't get anything but service name and
        # service tags from previous one ... unfortunately). catalog.service()
        # returns (INDX, [NODE1, ...]), where NODEx is a dict
        chk_svcs = []
        for svc_name in chk_svc_names:
            chk_svcs += con.catalog.service(svc_name)[1]

        # now we have the consul "service" dicts in a list. let's filter them -
        # again - by check_tag (kinda super kinky, but *in theory* we can have
        # a service which is created by rancon, and an alternative which is
        # not. we only want to remove the one fro rancon, right?
        filtered = filter(
            lambda x: 'ServiceTags' in x and check_tag in x['ServiceTags'],
            chk_svcs
        )

        for chk_svc in filtered:
            # fields: Service{Port,Tags,ID,Name,Address}
            # The 'Address' field (withOUT 'Service' prefix!) depicts the
            # responsible consul node it seems!! So let's use this for
            # de-registering, maybe??
            if chk_svc['ServiceID'] not in keep_services:
                self.log.warn("CLEANUP: de-registering service id {}/{}:{}"
                              .format(chk_svc['ServiceID'],
                                      chk_svc['ServiceAddress'],
                                      chk_svc['ServicePort']))
                consul_inst = self._get_consul_for(
                    self._convert_to_service(chk_svc))
                consul_inst.agent.service.deregister(chk_svc['ServiceID'])

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

    @staticmethod
    def _convert_to_service(consul_service):
        return DotMap({
            'host': consul_service['ServiceAddress'],
            'port': consul_service['ServicePort'],
            'name': consul_service['ServiceName'],
            'tags': consul_service['ServiceTags'],
            'id':   consul_service['ServiceID'],
        })

def get():
    """ returns this model's main class """
    return ConsulBackend
