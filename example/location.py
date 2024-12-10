import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import tempfile
from functools import partial
from packaging.version import Version
from pymobiledevice3.services.simulate_location import DtSimulateLocation
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
from pymobiledevice3.services.mobile_image_mounter import DeveloperDiskImageMounter, MobileImageMounterService, \
    PersonalizedImageMounter, auto_mount
from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
from pymobiledevice3.lockdown_service_provider import LockdownServiceProvider
from pymobiledevice3.remote.tunnel_service import RemotePairingQuicTunnel, start_tunnel
from pymobiledevice3.remote.common import ConnectionType, TunnelProtocol
from pymobiledevice3.tunneld import TUNNELD_DEFAULT_ADDRESS, TunneldRunner, async_get_tunneld_devices
from pymobiledevice3.exceptions import InvalidServiceError, TunneldConnectionError
from pymobiledevice3.osu.os_utils import get_os_utils
from pymobiledevice3.usbmux import select_devices_by_connection_type
from pymobiledevice3.lockdown import create_using_usbmux, create_using_tcp


def start_tunnel(host, port, protocol):
    host = TUNNELD_DEFAULT_ADDRESS[0]
    port = TUNNELD_DEFAULT_ADDRESS[1]
    protocol = TunnelProtocol(protocol)

    if not get_os_utils().is_admin:
        raise RuntimeError('Please run as admin')
    tunneld_runner = partial(TunneldRunner.create,
        host,
        port,
        protocol=protocol,
        usb_monitor=True,
        wifi_monitor=True,
        usbmux_monitor=True,
        mobdev2_monitor=True,
    )
    
    if get_os_utils()._os_name != 'win32':
        from daemonize import Daemonize
        with tempfile.NamedTemporaryFile("wt") as pid_file:
            daemon = Daemonize(
                app=f"Tunneld {host}:{port}", 
                pid=pid_file.name, 
                action=tunneld_runner)
            daemon.start()
    else:
        tunneld_runner()
        

def idevice(udid=None, connection_type='USB'):
    devices = select_devices_by_connection_type(connection_type=connection_type)
    if udid is None and len(devices) == 1:
        return devices[0]

    for dev in devices:
        if dev.serial == udid:
            return dev

    raise RuntimeError(f'Device with udid {udid} not found')


def make_dvt_service(idevice, host, port):
    rsds = asyncio.run(async_get_tunneld_devices((host, port)))
    service_provider = [rsd for rsd in rsds if rsd.udid == idevice.serial][0]
    return DvtSecureSocketProxyService(service_provider)

def mounter_ddi(idevice):
    asyncio.run(auto_mount(idevice.lockdown), debug=True)

def done():
    print('Done!')
    sys.exit(0)

if __name__ == '__main__':
    host = TUNNELD_DEFAULT_ADDRESS[0]
    port = TUNNELD_DEFAULT_ADDRESS[1]
    type = TunnelProtocol.TCP if sys.version_info >= (3, 13) else TunnelProtocol.QUIC

    if len(sys.argv) <= 1:
        sys.argv.append('set')

    if sys.argv[1] == 'tunnel':
        start_tunnel(host, port, type)
    else:
        idevice = idevice(None, connection_type='USB')
        idevice.lockdown = create_using_usbmux(serial=idevice.serial)

        if sys.argv[1] == 'mount':
            mounter_ddi(idevice)
            done()
        elif sys.argv[1] == 'umount':
            DeveloperDiskImageMounter(idevice.lockdown).umount()
            done()

        elif sys.argv[1] == 'unset':
            if Version(idevice.lockdown.product_version) < Version('17.0'):
                DtSimulateLocation(idevice.lockdown).clear()
                done()
            else:
                print('Wait a minute...')

        else:
            if Version(idevice.lockdown.product_version) < Version('17.0'):
                try:
                    DtSimulateLocation(idevice.lockdown).set(40.690008, -74.045843)
                    done()
                except InvalidServiceError:
                    print('LocationSimulation service not available or need DeveloperDiskImage to be installed')
            else:
                try:
                    with make_dvt_service(idevice, host, port) as dvt:
                        location = LocationSimulation(dvt)
                        location.set(40.690008, -74.045843)
                        get_os_utils().wait_return()
                        location.clear()
                except TunneldConnectionError:
                    print('Tunneld service not available')
