# import providers, services and models
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from datetime import timedelta

from argparse import ArgumentParser
from urllib.parse import urlparse
import logging

"""
Create configuration for model Cisco-IOS-XR-segment-routing-ms-cfg.
usage: nc-create-xr-segment-routing-ms-cfg-10-ydk.py [-h] [-v] device
positional arguments:
  device         NETCONF device (ssh://user:password@host:port)
optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

if __name__ == "__main__":
    """Main execution path"""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                       "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF session
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)

    # provider = NetconfServiceProvider(address="10.20.0.170",
    #                                   port=22,
    #                                   username="system",
    #                                   password="system",
    #                                   protocol="ssh")

    # create CRUD service
    crud = CRUDService()

    # create system time object
    system_time = xr_shellutil_oper.SystemTime()
    # read system time from device
    system_time = crud.read(provider, system_time)

    # Print system time
    print("System uptime is " +
          str(timedelta(seconds=system_time.uptime.uptime)))
