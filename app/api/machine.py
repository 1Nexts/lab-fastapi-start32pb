from fastapi import APIRouter, Form, Depends, UploadFile, File,HTTPException
from pydantic import BaseModel
from typing import Optional
from app.api import schema
from sqlalchemy import asc, desc
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.Machine import Machine as MachineDB
from app.api import security
from pathlib import Path
import os
import shutil
from datetime import datetime

router = APIRouter()

def get_machine_form(
        id: Optional[int] = Form(None),
        name: str = Form(...),
        temperature: int = Form(...),
        sensor_a: int = Form(...),
        sensor_b: int = Form(...),
        status: int = Form(...)):
    return schema.Machine(id=id, name=name, temperature=temperature, sensor_a=sensor_a, sensor_b=sensor_b, status=status)


@router.get("/")
def get_machines(db: Session = Depends(get_db)):
    try:
        machine_db = db.query(MachineDB).order_by(asc("id"))

        return machine_db.all()
    except Exception as e:
        print("=== error get_machines ",str(e))
        raise HTTPException(
            status_code=404,
            detail="Get machines error please try again",
        )
        # return {"machine": "fail", "error": str(e)}


@router.get("/{id}")
async def get_machine_by_id(id: str, db: Session = Depends(get_db)):
    try:
        machine = db.query(MachineDB).filter(MachineDB.id == id).first()
        return machine
    except Exception as e:
        print("=== error get_machines_by_id ",str(e))
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

# @router.get("/rawsql/{id}")
# def get_machineRaw(id: str, db: Session = Depends(get_db)):
#     try:
#         result = db.execute("""
#         SELECT  
#         * FROM machines 
#         WHERE machines.id = {}""".format(id))

#         # results_as_dict = result.mappings().all()
#         # print(results_as_dict)
#         # print("=====")
#         # return results_as_dict;
#         arrResult = result.fetchall()
#         # if len(arrResult) == 0 :
#         #     return 'null'
#         return arrResult
#     except Exception as e:
#         print("=== error get_machineRaw ",str(e))
#         raise HTTPException(
#             status_code=404,
#             detail="Machine not found",
#         )

@router.post("/")
async def insert_machine(machine: schema.Machine = Depends(get_machine_form),
                         db: Session = Depends(get_db)):
    try:
        machine_db = MachineDB(**machine.dict())
        db.add(machine_db)
        db.commit()

        # return machine_db.as_dict()
        return {
            'result':'ok',
            'detail':'Create machine success',
            'data':machine_db.as_dict()
        }
    except Exception as e:
        print("=== error insert_machine ",str(e))
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )


@router.put("/")
async def update_machine(machine: schema.Machine = Depends(get_machine_form),
                         db: Session = Depends(get_db)):
    try:
        # update meta
        machine_db = db.query(MachineDB).filter(MachineDB.id == machine.id)
        machine_db.update({MachineDB.name: machine.name,
                           MachineDB.temperature: machine.temperature,
                           MachineDB.sensor_a: machine.sensor_a,
                           MachineDB.sensor_b: machine.sensor_b,
                           MachineDB.status: machine.status,
                           MachineDB.updated_at: datetime.now()})
        db.commit()

        # return machine_db.first().as_dict()
        # return product_db.first().as_dict()
        return {
            'result':'ok',
            'detail':'Update machine success',
            'data': machine_db.first().as_dict()
        }
    except Exception as e:
        print("=== error update_machine ",str(e))
        raise HTTPException(
            status_code=404,
            detail="Update machine fail",
        )


@router.delete("/{id}")
async def delete_machine(id: str, db: Session = Depends(get_db)):
    try:
        machines = db.query(MachineDB).filter(MachineDB.id == id)
        machines.delete()
        db.commit()
        return {
            'result':'ok',
            'detail':'Delete machine success'
        }
    except Exception as e:
        print("=== error delete_machine ",str(e))
        raise HTTPException(
            status_code=404,
            detail="Delete machine fail",
        )
