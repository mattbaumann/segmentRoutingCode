# import providers, services and models
from datetime import timedelta
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from ydk.models.ietf import ietf_interfaces

if __name__ == "__main__":
    """Main execution path"""

    # create NETCONF session
    provider = NetconfServiceProvider(address="10.20.0.170",
                                      port=22,
                                      username="system",
                                      password="system",
                                      protocol="ssh")

    # create CRUD service
    crud = CRUDService()

    # Top Level Object
    system_time = xr_shellutil_oper.SystemTime()
    interface_name = ietf_interfaces.Interfaces()

    # read system time from device
    system_time = crud.read(provider, system_time)
    interface_name = crud.read(provider, interface_name)

    # Print system time
    print("System uptime is " + str(timedelta(seconds=system_time.uptime.uptime)))

    # TODO get interface name or description or something like that
    print("Interface is " + str(interface_name.interface['Loopback0'].name))

    exit()
