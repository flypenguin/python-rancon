from rancon.tools import fail

import importlib as il
from argparse import ArgumentParser as AP
from os import environ

args = None
backend = None
source = None


def _parse_params_opts_env(env_name):
    opts = environ.get(env_name, None)
    if opts:
        return opts.split(",")
    else:
        return []


def parse_params(sys_argv):
    global args
    global backend
    global source
    parser = AP()
    parser.add_argument("-d", "--domain",
                        help="The domain to check for. Example: If set to 'my."
                             "domain.com', then the load balancer will react to"
                             "'servicename.my.domain.com'. CURRENTLY UNUSED.",
                        action="append")
    parser.add_argument("source",
                        help="Which source to use. Available are: 'rancher'. "
                             "Default: $RANCON_SOURCE or 'rancher'",
                        default=environ.get("RANCON_SOURCE", None))
    parser.add_argument("backend",
                        help="Which service backend (registry) to use. "
                             "Available are: 'consul'. "
                             "Default: $RANCON_BACKEND",
                        default=environ.get("RANCON_REGISTRY", None))
    parser.add_argument("-s", "--source-option",
                        help="Specify options for the available sources. "
                             "Default: $SOURCE_OPTIONS (which should look "
                             "like 'O1=V1,O2=V2,...')",
                        action="append",
                        default=_parse_params_opts_env('FRONTEND_OPTIONS '))
    parser.add_argument("-b", "--backend-option",
                        help="Specify options for the available registries. "
                             "Default: $REGISTRY_OPTIONS (which should look "
                             "like 'O1=V1,O2=V2,...')",
                        action="append",
                        default=_parse_params_opts_env('BACKEND_OPTIONS'))

    args = parser.parse_args(sys_argv)
    errors = []

    # get parameters
    args.backend_options = dict([d.split("=", 1) for d in args.backend_option])
    args.source_options = dict([d.split("=", 1) for d in args.source_option])
    del args.backend_option
    del args.source_option

    # check required SOURCE and REGISTRY settings
    classes = []
    for a in (("source", args.source, "-s", args.source_options),
              ("backend", args.backend, "-b", args.backend_options)):
        try:
            i = il.import_module("rancon.{}s.{}".format(a[0], a[1]))
            got_class = i.get()
            for ropt in got_class.required_opts:
                if ropt not in a[3]:
                    errors.append("Missing required '{}' option: {} {}=..."
                                  .format(a[1], a[2], ropt))
        except ImportError:
            errors.append("Invalid source type: {}".format(args.backend))

        if len(errors) == 0:
            classes.append(got_class(**a[3]))

    if errors:
        fail(errors)
    else:
        source, backend = classes[0], classes[1]
