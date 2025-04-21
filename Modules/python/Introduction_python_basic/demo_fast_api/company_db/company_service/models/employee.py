from pydantic import BaseModel


# Pydantic models
class Employee(BaseModel):
    name: str
    email: str
    department: str

class EmployeeWithID(Employee):
    id: int
