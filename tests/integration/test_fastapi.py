import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_fastapi(
    client_fastapi: TestClient,
) -> None:
    data = [
        {
            "message_id": 1,
            "text": "New MESSAGE222",
            "command": "/start",
        },
    ]
    res = client_fastapi.post("/res", json=data)
    assert res.status_code == 200