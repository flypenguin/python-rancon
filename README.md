# Rancon

Takes information from currently rancher and forwards it into a service registry (currently consul). I currently use this to configure dynamic routing into rancher services.

Documentation is pretty incomplete, but might be self-explanatory if called.

    python -m rancon --help


## Super quick start

- clone rancon
- add a service in rancher
    - assign a label `rancon` with any value
- start rancon `python -m rancon rancher consul -s url=rancherurl -b url=consulurl`
- look at the output, and in consul
- upgrade the service, and change the labels to ``rancon.name=supercool``.
- start again, look at the output, and in consul


## More details of operation

The basic calling scheme is:

    python -m rancon SOURCE_SERVICE BACKEND_SERVICE \
        -s SOURCE_PARAM=VALUE \
        -b BACKEND_PARAM=VALUE

... whereas SOURCE_PARAM and BACKEND_PARAM can be specified multiple times.

Currently only ``rancher`` exists as "source" service, and only ``consul`` exists as "backend" service.

Rancon goes through the "source" service (for now only Rancher) and looks for services which have a label attached matching 'rancon(\..*)?'. If this label is attached the service is entered into the backend (for now only consul :).

The operation can also be controlled by those tags. Each "source" provides different information to the backend, whereas the following information is always present:

- ``name``, can be overwritten (string)
- ``host``, can not be overwritten (string)
- ``port``, can not be overwritten (string)
- ``source``, can not be overwritten (complex, invisible to the user)


## Additional service information

### 'Rancher' source

Additionally to the above mentioned items the following is also set on each service:

- ``stack``
- ``environment``

You can add additional information to each service simply by setting a label ``rancon.X``. Now each service gets an "X" property when being registered in the backend (Consul), which might be processed by the backend.


## Special tags for backends

### 'Consul' backend

Currently only the ``name`` tag is used from the service. The name tag can contain placeholders to influence naming (see below).


## Using the service information in tags

The registration process in the backend can be controlled using tags.

Example: Your service is named "myservice", in a stack called "teststack". If you tag a service in Rancher with ``rancon.name=%NAME%-%STACK%``, the service will be registered in Consul under the name ``myservice-teststack``.


## State

WORKING:

- discovery
- entry of services in Consul
- cleanup of Consul-services if their counterpart is no longer present in Rancher
- authentication with Rancher

NONWORKING:

- consul with TLS

PLANNED:

- traefik support
- maybe a more generic approach, cause this forwarding thing might be useful for more than just load balancing
- add tests (currently completely untested ... really bad)
