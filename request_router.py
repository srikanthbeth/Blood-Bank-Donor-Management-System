from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from database import get_db
from dependencies import staff_only

router = APIRouter(
    prefix="/requests",
    tags=["Blood Requests"]
)


@router.post(
    "",
    response_model=schemas.BloodRequestResponse
)
def create_request(
    request: schemas.BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):
    return crud.create_request(db, request)


@router.get(
    "",
    response_model=list[schemas.BloodRequestResponse]
)
def get_requests(
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):
    return crud.get_requests(db)


@router.get(
    "/{request_id}",
    response_model=schemas.BloodRequestResponse
)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):

    request = crud.get_request(db, request_id)

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return request


@router.put(
    "/{request_id}",
    response_model=schemas.BloodRequestResponse
)
def update_request(
    request_id: int,
    request: schemas.BloodRequestUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):

    updated = crud.update_request(
        db,
        request_id,
        request
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return updated