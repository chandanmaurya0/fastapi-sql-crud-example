from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel


from routers import flight_route, user_route

app = FastAPI()


app.include_router(user_route.router)
app.include_router(flight_route.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def read_item():
    return {"status": "API is live!"}
