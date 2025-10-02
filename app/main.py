import os
from app.Api.router import api_router
import multiprocessing
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Persistance.database_initialization import initialize_database
from app.Configuration.Helpers.tools import get_enviromental_variable
from app.Security.auth_middleware import AuthMiddleware
from app.Security.jwt_handler import JWTHandler

#Saving Processes to terminate them later
cache_processes:List[multiprocessing.Process] = []

# Custom fast API fields.
api_path = get_enviromental_variable("API_PATH")
app = FastAPI(
    title=get_enviromental_variable("NAME"),
    version=get_enviromental_variable("API_VERSION"),
    description=get_enviromental_variable("DESCRIPTION"),
    openapi_url=f"{api_path}/openapi.json",
    docs_url=f"{api_path}/docs",
    redoc_url=f"{api_path}/redoc",
    debug=True,
)

# Set all CORS enabled origins.
# if configuration.BACKEND_CORS_ORIGINS:
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(router=api_router, prefix=api_path)
app.middleware("http")(AuthMiddleware)
app.middleware("https")(AuthMiddleware)


initialize_database()
