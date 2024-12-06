import sys
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
from pymobiledevice3.lockdown_service_provider import LockdownServiceProvider


if __name__ == '__main__':
    service_provider = RemoteServiceDiscoveryService(rsd)
    with DvtSecureSocketProxyService(service_provider) as dvt:
        LocationSimulation(dvt).set(40.690008, -74.045843)
        
        # TODO
        LocationSimulation(dvt).clear()