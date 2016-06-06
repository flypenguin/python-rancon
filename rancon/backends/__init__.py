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

    def cleanup(self):
        """
        Performs 'garbage collection' of no-longer-present services. (If a
        service was registered in a previous run, and is no longer present, it
        might have to be removed manually).
        :return: True on success
        """
        pass
