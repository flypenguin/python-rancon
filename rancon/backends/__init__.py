class BackendBase(object):

    def register(self, service):
        """
        Registers a service in the backend.
        :param service: A rancon.service.Service instance
        :return: None
        """
        pass

    def cleanup(self):
        pass

