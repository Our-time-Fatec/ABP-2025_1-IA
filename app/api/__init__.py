# app/api/__init__.py
from app.api.routes.nvdi_route import router as ndvi_router


routers = [ndvi_router]
