from fastapi import FastAPI

from app.router.global_router import router as def_route
from app.router.global_router import calc_router

app = FastAPI()
app.include_router(def_route)
app.include_router(calc_router)
