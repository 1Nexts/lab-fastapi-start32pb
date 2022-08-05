from fastapi import FastAPI
from app.api.v2 import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from app.config.setting import settings


app = FastAPI()
app.mount("/images", StaticFiles(directory="uploaded/images",
          html=True), name="images")

# app.mount("/images/employees", StaticFiles(directory="uploaded/images/employees",
#           html=True), name="images_employees")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    print("Cors settings : ", settings.BACKEND_CORS_ORIGINS)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    print("No cors settings")


# app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v2")
