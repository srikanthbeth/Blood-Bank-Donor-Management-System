from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models

from database import get_db
from dependencies import admin_only, donor_only

router = APIRouter(
    prefix="/donations",
    tags=["Donations"]
)


# =====================================================
# CREATE DONATION (ADMIN ONLY)
# =====================================================

@router.post(
    "",
    response_model=schemas.DonationResponse
)
def create_donation(
    donation: schemas.DonationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.create_donation(db, donation)


# =====================================================
# DONOR CAN VIEW ONLY THEIR OWN DONATION HISTORY
# =====================================================

@router.get(
    "/my-history",
    response_model=list[schemas.DonationResponse]
)
def my_history(
    db: Session = Depends(get_db),
    current_user=Depends(donor_only)
):
    donor = db.query(models.Donor).filter(
        models.Donor.user_id == current_user.id
    ).first()

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor profile not found"
        )

    return crud.get_my_donations(
        db,
        donor.id
    )