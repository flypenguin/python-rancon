class Service(object):

    def __init__(self, name, host, port, source, domain='', **kwargs):
        self.name = name
        self.host = host
        self.port = port
        self.source = source
        self.domain = domain
        self.meta = kwargs

    def __str__(self):
        return "{} ({}:{})".format(
            self.name, self.host, self.port
        )
