import asyncio
from typing import Generator

import pytest
import uvloop


@pytest.fixture(scope="session", autouse=True)
def uvloop_event_loop() -> Generator[uvloop.Loop, None, None]:
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
