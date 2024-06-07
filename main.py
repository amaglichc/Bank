from fastapi import FastAPI, Request

from Routers.AuthRouter import router as AuthRouter
from Routers.WalletRouter import router as WalletRouter
from Routers.mainRouter import router as mainRouter

app = FastAPI(
    title="CoolProjectRealHype",
    description="Real cool project")
app.include_router(mainRouter)
app.include_router(AuthRouter)
app.include_router(WalletRouter)


@app.on_event("startup")
async def startup():
    print("startup")


@app.on_event("shutdown")
async def shutdown():
    print("shutdown")


@app.middleware("http")
async def add_time(request: Request, call_next):
    response = await call_next(request)
    return response
