# mypy: allow-untyped-defs

import pytest
import opennetzteil
from aiohttp import ClientResponseError

# The dummy device does not implement setting a value.
# For now we are happy when no http errors occur.


@pytest.fixture()
@pytest.mark.asyncio
async def client():
    return await opennetzteil.Netzteil.connect("http://localhost:8000", 1)


def test_probe(client):
    # Probing is done in the fixture.
    # Just query the result.
    assert client.ident == "dummy-device"


@pytest.mark.asyncio
async def test_get_channel(client):
    with pytest.raises(ClientResponseError):
        await client.get_channel(412389)
    on = await client.get_channel(1)
    assert on is True


@pytest.mark.asyncio
async def test_set_channel(client):
    with pytest.raises(ClientResponseError):
        await client.set_channel(412389, False)
    await client.set_channel(1, True)


@pytest.mark.asyncio
async def test_get_master(client):
    on = await client.get_channel(0)
    assert on is True
    on = await client.get_master()
    assert on is True


@pytest.mark.asyncio
async def test_set_master(client):
    await client.set_channel(0, False)
    await client.set_master(False)
