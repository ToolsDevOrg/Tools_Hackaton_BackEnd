from app.api.users import router as users_router
from app.api.passes import router as passes_router

all_routers = [
    users_router,
    passes_router
]

