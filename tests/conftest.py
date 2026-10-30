import pytest_asyncio
from agents import set_tracing_disabled
from agent_client import make_server


@pytest_asyncio.fixture
async def server(tmp_path):
    set_tracing_disabled(True)
    async with make_server(tmp_path / "records", verbose=False) as connected:
        yield connected
