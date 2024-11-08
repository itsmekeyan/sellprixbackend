from fastapi.routing import APIRouter

from fast_api.web.api import docs, echo, monitoring, frappe

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(frappe.router, tags=["frappe"])
