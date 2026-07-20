from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from database import get_db
from dependencies import admin_only

router = APIRouter(
    prefix="/donors",
    tags=["Donors"]
)


@router.post(
    "",
    response_model=schemas.DonorResponse
)
def create_donor(
    donor: schemas.DonorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.create_donor(db, donor)


@router.get(
    "",
    response_model=list[schemas.DonorResponse]
)
def get_all_donors(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    skip = (page - 1) * limit
    return crud.get_donors(db, skip, limit)


@router.get(
    "/{donor_id}",
    response_model=schemas.DonorResponse
)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    donor = crud.get_donor(db, donor_id)

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return donor


@router.put(
    "/{donor_id}",
    response_model=schemas.DonorResponse
)
def update_donor(
    donor_id: int,
    donor: schemas.DonorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    updated = crud.update_donor(
        db,
        donor_id,
        donor
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return updated


@router.delete("/{donor_id}")
def delete_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    donor = crud.delete_donor(db, donor_id)

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return {
        "message": "Donor deleted successfully"
    }