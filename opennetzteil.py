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
    def connect(cls, host: str, device: int):
        baseurl = urljoin(host, cls.URL_PREFIX)
        s = requests.Session()
        u = urljoin(baseurl, f"/devices/{device}/ident")
        r = s.get(u)
        r.raise_for_status()
        ident = r.json()
        return cls(s, host, ident, device)

    def set_channel(self, channel: int, enabled: bool):
        u = urljoin(self.baseurl, f"/devices/{self.device}/channel/{channel}")
        r = self.session.put(u, json=enabled)
        r.raise_for_status()

    def get_channel(self, channel: int) -> bool:
        u = urljoin(self.baseurl, f"/devices/{self.device}/channel/{channel}")
        r = self.session.get(u)
        r.raise_for_status()
        return r.json()
