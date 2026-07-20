from fastapi import FastAPI

import models

from database import engine
from routers import auth_router, donor_router, inventory_router, request_router, report_router, donation_router
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blood Bank & Donor Management System"
)
app.include_router(auth_router.router)
app.include_router(donor_router.router)
app.include_router(inventory_router.router)
app.include_router(request_router.router)
app.include_router(report_router.router)
app.include_router(donation_router.router)

@app.get("/")
def root():
    return {
        "message": "Blood Bank API Running Successfully"
    }