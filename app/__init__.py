from fastapi import FastAPI

from app.config import API_PREFIX, VERSION, DEVICE_ROUTER_PREFIX, CALC_PROFIT_ROUTER_PREFIX
from app.router.global_router import router as def_route
from app.router.global_router import calc_router

app = FastAPI(
    docs_url=f'{API_PREFIX}/docs',
    title="Collector.small",
    version=f'{VERSION}',
    openapi_url=f'{API_PREFIX}/openapi.json'
)

app.include_router(
    def_route,
    prefix=f'{API_PREFIX}{DEVICE_ROUTER_PREFIX}',
    tags=['devices_by_ip'],
)

app.include_router(
    calc_router,
    prefix=f'{API_PREFIX}{CALC_PROFIT_ROUTER_PREFIX}',
    tags=['calc_profit_service']
)
