# app/api/__init__.py
from routes.nvdi_route import router as ndvi_router


routers = [ndvi_router]
