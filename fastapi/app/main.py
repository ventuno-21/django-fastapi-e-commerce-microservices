from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import r_auth, r_user
from .routers.deps import get_current_user
from .database.schemas import MeResponse
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup tasks
    print("FastAPI auth service starting...")
    yield
    # shutdown tasks
    print("FastAPI auth service shutting down...")


app = FastAPI(title="FastAPI User & Auth Service", lifespan=lifespan)

# CORS - allow for local dev & frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(r_auth.router)
app.include_router(r_user.router)


# /me shortcut used by other services (e.g. Django)
@app.get("/me", response_model=MeResponse)
async def me_dep(current_user=Depends(get_current_user)):
    return MeResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
    )
