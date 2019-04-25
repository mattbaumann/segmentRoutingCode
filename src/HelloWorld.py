# import providers, services and models
from datetime import timedelta
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_crypto_ssh_oper as ssh_oper

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
    ssh_config = ssh_oper.Ssh()

    # read system time from device
    system_time = crud.read(provider, system_time)
    ssh_config = crud.read(provider, ssh_config)

    # Print system time
    print("System uptime is " + str(timedelta(seconds=system_time.uptime.uptime)))
    print("Test " + system_time.uptime.host_name)

    # for item in ssh_config.session.rekey.incoming_sessions.session_rekey_info:
    #     print(item.session_id)

    for item in ssh_config.session.history.incoming_sessions.session_history_info:
        print(item.authentication_type)

    for item in ssh_config.session.detail.incoming_sessions.session_detail_info:
        print(item.key_exchange)

    exit()
