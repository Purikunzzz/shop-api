from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import user_router, product_router, order_router

from app.models import User, Product, Order

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database Ready")
    yield # app is running

    await engine.dispose()
    print("Shutting Down")

app = FastAPI(
    title="Shop API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect all routers
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

@app.get("/")
async def root():
    return {"message": "Shop API is running"}