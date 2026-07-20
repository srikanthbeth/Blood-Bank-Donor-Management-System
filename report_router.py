from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud

from database import get_db
from dependencies import admin_only

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/donors")
def search_donors(
    blood_group: str = None,
    city: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    skip = (page - 1) * limit

    return crud.search_donors(
        db,
        blood_group,
        city,
        skip,
        limit
    )


@router.get("/requests")
def filter_requests(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    skip = (page - 1) * limit

    return crud.filter_requests(
        db,
        status,
        skip,
        limit
    )


@router.get("/inventory")
def inventory_report(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.blood_stock_report(db)