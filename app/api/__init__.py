# app/api/__init__.py
from app.api.routes.nvdi_route import router as ndvi_router
from app.api.routes.status_route import router as status_router


routers = [ndvi_router, status_router]
