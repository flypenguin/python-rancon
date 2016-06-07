from re import compile


tag_matcher = compile("%META.([A-Z0-9]+)%")


class BackendBase(object):

    required_opts = ()
    additional_opts = ()

    def register(self, service):
        """
        Registers a service in the backend.
        :param service: A rancon.service.Service instance
        :return: None
        """
        pass

    def cleanup(self, keep_services):
        """
        Performs 'garbage collection' of no-longer-present services. (If a
        service was registered in a previous run, and is no longer present, it
        might have to be removed manually).
        :param keep_services: A list of services to keep. Each service in the
        list is a return value from register(), which can be pretty much
        anything.
        :return: An integer how many services have been removed.
        """
        pass

    @staticmethod
    def _tag_map(tag, service):
        """
        Replaces a tag content with replacement information from the service.
        The replacement must exist. If you want to use a value form the
        service.meta dict, just use the value 'META.<KEYNAME>' as tag
        replacement string.
        :param tag: The tag value
        :param service: The service to use for the replacements
        :return: The processed tag value
        """
        tmp = tag.replace("%NAME%", service.name) \
            .replace("%HOST%", service.host) \
            .replace("%PORT%", str(service.port))
        metavars = tag_matcher.findall(tag)
        for meta in metavars:
            tmp = tmp.replace("%META.{}%".format(meta),
                              service.meta[meta.lower()])
        return tmp

    @staticmethod
    def _get_cleanup_tag_for(service_id):
        return "rancon_cleanup_id_{}".format(service_id)
