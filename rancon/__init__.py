"""
Crawl through all available rancher services and look for a label with
the following format:

    rancon.consul.service: SERVICE_NAME
    rancon.consul.tag: TAG_NAME

If a service with this tag is found, it will be published as service
"SERVICE_NAME" in Consul, and the service will get the tag TAG_NAME (if
set).

*All* services created by rancon will be tagged "rancon" in consul, so that
rancon is able to remove services which are no longer available in rancher.

"""

import cattleprod

import sys
from os import environ
from argparse import ArgumentParser as AP


args = None


def fail(message):
    print("FATAL:%s" % message)
    sys.exit(-1)


def keep_running():
    pass



def parse_params(sys_argv):
    global args
    parser = AP()
    parser.add_argument("-s", "--rancher-secret-key",
                        help="Rancher secret key to use. *Required*. "
                             "Default: $RANCHER_SECRET_KEY",
                        default=environ.get("RANCHER_SECRET_KEY", None))
    parser.add_argument("-a", "--rancher-access-key",
                        help="Rancher access key to use. *Required*. "
                             "Default: $RANCHER_ACCESS_KEY",
                        default=environ.get("RANCHER_ACCESS_KEY", None))
    parser.add_argument("-u", "--rancher-url",
                        help="URL for the Rancher API. *Required*. "
                             "Default: $RANCHER_URL",
                        default=environ.get("RANCHER_URL", None))
    args = parser.parse_args(sys_argv)
    errors = []
    if not args.rancher_access_key:
        errors.append("$RANCHER_ACCESS_KEY not set.")
    if not args.rancher_secret_key:
        errors.append("$RANCHER_SECRET_KEY not set.")
    if not args.rancher_url:
        errors.append("$RANCHER_URL not set.")
    if errors:
        fail("\n    ".join(errors))


def start(sys_argv):
    parse_params(sys_argv)
    keep_running()


def console_entrypoint():
    start(sys.argv[1:])
