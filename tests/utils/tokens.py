from fastapi.testclient import TestClient

from app.api.v1.auth.utils import SecurityManager
from app.config import settings


async def get_access_token_headers() -> dict[str, str]:
    username = settings.FIRST_USER_USERNAME
    access_token = SecurityManager().create_access_token(data={"sub": username})
    return {"Authorization": f"Bearer {access_token}"}
