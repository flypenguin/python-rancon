from rancon.tools import fail

from argparse import ArgumentParser as AP
from os import environ

args = None


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
    parser.add_argument("-c", "--consul-url",
                        help="URL for the Consul API. "
                             "Default: $CONSUL_URL or 'localhost:8500'",
                        default=environ.get("CONSUL_URL", 'localhost:8500'))
    args = parser.parse_args(sys_argv)
    errors = []
    if not args.rancher_url:
        errors.append("$RANCHER_URL is not set.")
    if not args.consul_url:
        errors.append("$CONSUL_URL is not set.")
    if errors:
        fail("\n    ".join(errors))


