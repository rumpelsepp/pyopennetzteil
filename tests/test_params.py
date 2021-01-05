# mypy: allow-untyped-defs

import pytest
import opennetzteil
from requests import exceptions

# The dummy device does not implement setting a value.
# For now we are happy when no http errors occur.


@pytest.fixture()
def client():
    return opennetzteil.Netzteil.connect("http://localhost:8000", 1)


def test_probe(client):
    # Probing is done in the fixture.
    # Just query the result.
    assert client.ident == "dummy-device"


def test_get_channel(client):
    with pytest.raises(exceptions.HTTPError):
        client.get_channel(412389)
    on = client.get_channel(1)
    assert on is True


def test_set_channel(client):
    with pytest.raises(exceptions.HTTPError):
        client.set_channel(412389, False)
    client.set_channel(1, True)


def test_get_master(client):
    on = client.get_channel(0)
    assert on is True
    on = client.get_master()
    assert on is True


def test_set_master(client):
    client.set_channel(0, False)
    client.set_master(False)
