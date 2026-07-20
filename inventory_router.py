from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from database import get_db
from dependencies import staff_only


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post(
    "",
    response_model=schemas.InventoryResponse
)
def create_inventory(
    inventory: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):
    return crud.create_inventory(
        db,
        inventory
    )


@router.get(
    "",
    response_model=list[schemas.InventoryResponse]
)
def get_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):
    return crud.get_inventory(db)


@router.put(
    "/{inventory_id}",
    response_model=schemas.InventoryResponse
)
def update_inventory(
    inventory_id: int,
    inventory: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(staff_only)
):

    updated = crud.update_inventory(
        db,
        inventory_id,
        inventory
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    return updated  