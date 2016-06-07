from re import compile


tag_matcher = compile("%META.([A-Z0-9]+)%")


class CommonBase(object):

    @staticmethod
    def _tag_replace(tag, service):
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
