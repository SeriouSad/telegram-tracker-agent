from contextlib import asynccontextmanager
import logging
import asyncio

from fastapi import APIRouter, FastAPI

from src.api.v1.routers.subscription import router as subscription_router
from src.api.middlewares.auth import BasicAuthMiddleware

logger = logging.getLogger(__name__)


app = FastAPI(
    docs_url="/schema/swagger-ui",
    redoc_url="/schema/redoc",
    openapi_url="/schema/openapi.json",
)

router = APIRouter(prefix="/api/v1")
router.include_router(subscription_router)

app.include_router(router)

app.add_middleware(BasicAuthMiddleware)
