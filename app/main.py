import os
from app.Api.router import api_router
import multiprocessing
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Persistance.database_initialization import initialize_database
from app.Configuration.Helpers.tools import get_enviromental_variable
import asyncio
#Saving Processes to terminate them later
cache_processes:List[multiprocessing.Process] = []
# Custom fast API fields.
api_path = get_enviromental_variable("API_PATH")
fast_api = FastAPI(
    title=get_enviromental_variable("NAME"),
    version=get_enviromental_variable("API_VERSION"),
    description=get_enviromental_variable("DESCRIPTION"),
    openapi_url=f"{api_path}/openapi.json",
    debug=True,
)

# Set all CORS enabled origins.
# if configuration.BACKEND_CORS_ORIGINS:
fast_api.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

fast_api.include_router(router=api_router)

initialize_database()
