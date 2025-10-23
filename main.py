from fastapi import FastAPI
from db import Base, engine
from app.routers import products, categories

app = FastAPI(title="Smart WMS - Products & Categories")

@app.get("/")
def greet():
    return "Smart WMS API - Products & Categories"

app.include_router(products.router)
app.include_router(categories.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
