from __future__ import annotations
from urllib.parse import urljoin

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

    def set_channel(self, channel: int, enabled: bool) -> None:
        p = f"devices/{self.device}/channels/{channel}/out"
        u = urljoin(self.baseurl, p)
        r = self.session.put(u, json=enabled)
        r.raise_for_status()

    def get_channel(self, channel: int) -> bool:
        p = f"devices/{self.device}/channels/{channel}/out"
        u = urljoin(self.baseurl, p)
        r = self.session.get(u)
        r.raise_for_status()
        return r.json()

    def set_master(self, enabled: bool) -> None:
        return self.set_channel(0, enabled)

    def get_master(self) -> bool:
        return self.get_channel(0)
