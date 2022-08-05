from fastapi import APIRouter, Depends
from app.api import authen, employee, machine
from app.models import database
from app.api import security
database.Base.metadata.create_all(database.engine, checkfirst=True)

api_router = APIRouter()


api_router.include_router(authen.router,
                          tags=["authen"])

api_router.include_router(machine.router,
                          prefix="/machine",
                          tags=["machine"],
                          dependencies=[Depends(security.checkAuthorized)])

api_router.include_router(employee.router,
                          prefix="/employee",
                          tags=["employee"],
                          dependencies=[Depends(security.checkAuthorized)])

