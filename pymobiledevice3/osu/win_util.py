import datetime
import os
import socket
from pathlib import Path


from ifaddr import get_adapters

from pymobiledevice3.osu.os_utils import DEFAULT_AFTER_IDLE_SEC, DEFAULT_INTERVAL_SEC, OsUtils
from pymobiledevice3.usbmux import MuxConnection


class Win32(OsUtils):
    @property
    def is_admin(self) -> bool:
        try:
            import win32security

            """ Check if the current OS user is an Administrator or root.
            See: https://github.com/Preston-Landers/pyuac/blob/master/pyuac/admin.py
            :return: True if the current user is an 'Administrator', otherwise False.
            """
            try:
                admin_sid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid, None)
                return win32security.CheckTokenMembership(None, admin_sid)
            except Exception:
                return False
        except:
            return self.is_admin_by_ctypes()
        
    def is_admin_by_ctypes(self) -> bool:
        import ctypes
        try:
            WinBuiltinAdministratorsSid = 26  # Constant value for the administrator group SID
            SECURITY_NT_AUTHORITY = (ctypes.c_ubyte * 6)(0, 0, 0, 0, 0, 5)  # SECURITY_NT_AUTHORITY

            admin_sid = ctypes.c_void_p()
            ctypes.windll.advapi32.AllocateAndInitializeSid(
                ctypes.byref(SECURITY_NT_AUTHORITY), 2,
                0x20,   # SECURITY_BUILTIN_DOMAIN_RID
                0x220,  # DOMAIN_ALIAS_RID_ADMINS
                0, 0, 0, 0, 0, 0,
                ctypes.byref(admin_sid)
            )

            # Checks if the current user's token contains an administrator group
            is_admin = False
            is_member = ctypes.c_long(0)
            if ctypes.windll.advapi32.CheckTokenMembership(None, admin_sid, ctypes.byref(is_member)):
                is_admin = is_member.value != 0

            # free SID
            ctypes.windll.advapi32.FreeSid(admin_sid)
            return is_admin
        except:
            return False

    @property
    def usbmux_address(self) -> tuple:
        return MuxConnection.ITUNES_HOST, socket.AF_INET

    @property
    def bonjour_timeout(self) -> int:
        return 2

    @property
    def loopback_header(self) -> bytes:
        return b'\x00\x00\x86\xdd'

    @property
    def access_denied_error(self) -> str:
        return 'This command requires admin privileges. Consider retrying with "run-as administrator".'

    @property
    def pair_record_path(self) -> Path:
        return Path(os.environ.get('ALLUSERSPROFILE', ''), 'Apple', 'Lockdown')

    def get_ipv6_ips(self) -> list:
        # py 3.8 does not support ipv6's zone index
        # return [f'{adapter.ips[0].ip[0]}%{adapter.ips[0].ip[2]}' for adapter in get_adapters() if adapter.ips[0].is_IPv6]
        return [f'{adapter.ips[0].ip[0]}' for adapter in get_adapters() if adapter.ips[0].is_IPv6]

    def set_keepalive(self, sock: socket.socket, after_idle_sec: int = DEFAULT_AFTER_IDLE_SEC,
                      interval_sec: int = DEFAULT_INTERVAL_SEC, **kwargs) -> None:
        sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, after_idle_sec * 1000, interval_sec * 1000))

    def parse_timestamp(self, time_stamp) -> datetime:
        return datetime.datetime.fromtimestamp(time_stamp / 1000)

    def chown_to_non_sudo_if_needed(self, path: Path) -> None:
        return

    def wait_return(self):
        input('Press ENTER to exit>')
