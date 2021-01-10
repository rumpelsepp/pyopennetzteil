from __future__ import annotations
from urllib.parse import urljoin
from typing import Any, cast

import requests


class Netzteil:
    URL_PREFIX = "/_netzteil/api/"

    def __init__(self, session: requests.Session, host: str, ident: str,
                 device: int):
        self.host = host
        self.baseurl = urljoin(host, self.URL_PREFIX)
        self.device = device
        self.session = session
        self.ident = ident

    @classmethod
    def connect(cls, host: str, device: int) -> Netzteil:
        baseurl = urljoin(host, cls.URL_PREFIX)
        u = urljoin(baseurl, f"devices/{device}/ident")
        s = requests.Session()
        r = s.get(u)
        r.raise_for_status()
        ident = r.json()
        return cls(s, host, ident, device)

    def _put_value(self, endpoint: str, channel: int, value: Any) -> None:
        p = f"devices/{self.device}/channels/{channel}/{endpoint}"
        u = urljoin(self.baseurl, p)
        r = self.session.put(u, json=value)
        r.raise_for_status()

    def _get_value(self, endpoint: str, channel: int) -> Any:
        p = f"devices/{self.device}/channels/{channel}/{endpoint}"
        u = urljoin(self.baseurl, p)
        r = self.session.get(u)
        r.raise_for_status()
        return r.json()

    def set_channel(self, channel: int, enabled: bool) -> None:
        return self._put_value("out", channel, enabled)

    def get_channel(self, channel: int) -> bool:
        return cast(bool, self._get_value("out", channel))

    def set_master(self, enabled: bool) -> None:
        return self.set_channel(0, enabled)

    def get_master(self) -> bool:
        return self.get_channel(0)

    def set_current(self, channel: int, val: float) -> None:
        return self._put_value("out", channel, val)

    def get_current(self, channel: int) -> float:
        return cast(float, self._get_value("out", channel))

    def set_voltage(self, channel: int, val: float) -> None:
        return self._put_value("voltage", channel, val)

    def get_voltage(self, channel: int) -> float:
        return cast(float, self._get_value("voltage", channel))

    def set_ocp(self, channel: int, enabled: bool) -> None:
        return self._put_value("ocp", channel, enabled)

    def get_ocp(self, channel: int) -> bool:
        return cast(bool, self._get_value("ocp", channel))

    def set_ovp(self, channel: int, enabled: bool) -> None:
        return self._put_value("ovp", channel, enabled)

    def get_ovp(self, channel: int) -> bool:
        return cast(bool, self._get_value("ovp", channel))
