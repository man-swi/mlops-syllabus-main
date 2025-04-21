from fastapi import APIRouter


router = APIRouter(prefix="")

@router.get("/")
def hello_company():
    return {"Hello": "Company"}

@router.get("/company/{compant_name}")
def compant_name(company_name: str):
    return {"compant_name": company_name}