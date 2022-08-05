from fastapi import APIRouter, Form, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.api import schema
from sqlalchemy import desc,asc
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.Employee import Employee as EmployeeDB
from app.api import security
from pathlib import Path
import os
import shutil
from datetime import datetime

router = APIRouter()


def get_employee_form(
        id: Optional[int] = Form(None),
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        gender: str = Form(...),
        province_id: int = Form(...),
        date_of_birth: str = Form(...),
        stack_interest: Optional[list[str]] = Form([]),
        note: Optional[str] = Form("")):
    return schema.Employee(id=id, first_name=first_name, last_name=last_name, email=email, phone=phone, gender=gender, province_id=province_id, date_of_birth=date_of_birth, stack_interest=stack_interest, note=note, image="")


def save_upload_file(upload_file: UploadFile, id: str) -> str:
    try:
        fileName = "{}.jpg".format(id)
        dest = Path(
            os.getcwd() + "/uploaded/images/employees/{}".format(fileName))
        with dest.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return fileName
    finally:
        upload_file.file.close()


def delete_upload_file(fileName: str) -> None:
    filePath = os.getcwd() + "/uploaded/images/employees/{}".format(fileName)
    if os.path.exists(filePath):
        os.remove(filePath)


@router.get("/")
def get_employee(db: Session = Depends(get_db)):

    try:
        employee_db = db.query(EmployeeDB).order_by(asc("id"))
        return employee_db.all()
    except Exception as e:
        print("=== error get_employee ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Get employee error please try again",
        )


@router.get("/{id}")
async def get_employee_id(id: str, db: Session = Depends(get_db)):
    try:
        employee = db.query(EmployeeDB).filter(EmployeeDB.id == id).first()
        return employee
    except Exception as e:
        print("=== error get_employee_id ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )


@router.post("/")
async def insert_employee(employee: schema.Employee = Depends(get_employee_form),
                          image: UploadFile = File(...),
                          db: Session = Depends(get_db)):
    try:
        db_employee = EmployeeDB(**employee.dict())
        db.add(db_employee)
        db.commit()

        if image:
            fileName = save_upload_file(image, db_employee.id)
            employee_db = db.query(EmployeeDB).filter(
                EmployeeDB.id == db_employee.id)
            employee_db.update({EmployeeDB.image: fileName})
            db.commit()

        # return db_employee.as_dict()
        return {
            'result': 'ok',
            'detail': 'Create employee success',
            'data': db_employee.as_dict()
        }
  
    except Exception as e:
        print("=== error insert_employee ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Duplicate email",
        )


@router.delete("/{id}")
async def delete_employee(id: str, db: Session = Depends(get_db)):
    try:
        employees = db.query(EmployeeDB).filter(EmployeeDB.id == id)
        imageFile = employees.first().image

        delete_upload_file(imageFile)
        employees.delete()
        db.commit()
        # return {"result": "ok"}
        return {
            'result': 'ok',
            'detail': 'Delete employee success'
        }

    except Exception as e:
        # return {"employee": "nok", "error": str(e)}
        print("=== error delete_employee ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Delete employee fail",
        )


@router.put("/")
async def update_employee(employee: schema.Employee = Depends(get_employee_form),
                          image: Optional[UploadFile] = File(None),
                          db: Session = Depends(get_db)):
    try:
        # update meta
        employee_db = db.query(EmployeeDB).filter(EmployeeDB.id == employee.id)
        employee_db.update({EmployeeDB.first_name: employee.first_name,
                           EmployeeDB.last_name: employee.last_name,
                           EmployeeDB.email: employee.email,
                           EmployeeDB.phone: employee.phone,
                           EmployeeDB.gender: employee.gender,
                           EmployeeDB.province_id: employee.province_id,
                           EmployeeDB.date_of_birth: employee.date_of_birth,
                           EmployeeDB.stack_interest: employee.stack_interest,
                           EmployeeDB.note: employee.note,
                           EmployeeDB.updated_at: datetime.now()})

        db.commit()

        # Update image name in db
        if image:
            save_upload_file(image, employee.id)

        # return employee_db.first().as_dict()
        return {
            'result': 'ok',
            'detail': 'Update employee success',
            'data': employee_db.first().as_dict()
        }
    except Exception as e:
        print("=== error update_employee ", str(e))
        raise HTTPException(
            status_code=404,
            detail="Update employee fail",
        )


# @router.get("/rawsql/{id}")
# def get_employeeRaw(id: str, db: Session = Depends(get_db)):
#     try:
#         print("=====")
#         result = db.execute("""
#         SELECT
#         * FROM employees
#         WHERE employees.id = {}""".format(id))

#         return result.fetchall()
#     except Exception as e:
#         return {"employee": "fail", "error": str(e)}
