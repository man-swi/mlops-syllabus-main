from fastapi import FastAPI
from company_service.router import router

app = FastAPI()

app.include_router(router)
