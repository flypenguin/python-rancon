class Service(object):

    def __init__(self, name, host, port, source, domain='', **kwargs):
        self.name = name
        self.host = host
        self.port = port
        self.source = source
        self.domain = domain
        self.other = kwargs
