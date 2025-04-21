from fastapi import APIRouter, Request
from company_service.models.employee import Employee, EmployeeWithID
from typing import List
import sqlite3

router = APIRouter(prefix="")

# API routes
# TODO: Please identify and fix the bug in this function
@router.get("/employees", response_model=List[Employee])
def get_employees(request: Request):
    cursor = request.app.state.db.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("SELECT id, name, email, department FROM employees")
    employees = [EmployeeWithID(**employee) for employee in cursor.fetchall()]
    return employees

@router.post("/employees", response_model=Employee)
def create_employee(request: Request, employee: Employee):
    cursor = request.app.state.db.cursor()
    cursor.execute("INSERT INTO employees (name, email, department) VALUES (?, ?, ?)",
                   (employee.name, employee.email, employee.department))
    request.app.state.db.commit()
    return employee

@router.put("/employees/{employee_id}", response_model=Employee)
def update_employee(request: Request, employee_id: int, employee: Employee):
    cursor = request.app.state.db.cursor()
    cursor.execute("UPDATE employees SET name = ?, email = ?, department = ? WHERE id = ?",
                   (employee.name, employee.email, employee.department, employee_id))
    request.app.state.db.commit()
    return employee

@router.delete("/employees/{employee_id}")
def delete_employee(request: Request, employee_id: int):
    cursor = request.app.state.db.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    request.app.state.db.commit()
    return {"message": "Employee deleted successfully"}