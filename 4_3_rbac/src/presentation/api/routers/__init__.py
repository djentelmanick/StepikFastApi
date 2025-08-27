from src.presentation.api.routers.admin import router as admin_router
from src.presentation.api.routers.auth import router as auth_router
from src.presentation.api.routers.guest import router as guest_router
from src.presentation.api.routers.resource import router as resource_router
from src.presentation.api.routers.user import router as user_router

list_routers = [
    auth_router,
    admin_router,
    user_router,
    guest_router,
    resource_router,
]
