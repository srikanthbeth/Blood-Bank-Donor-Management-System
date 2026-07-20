from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date

import models
import schemas
from auth import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def create_user(db: Session, user: schemas.UserRegister):

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

from datetime import date

# =====================================================
# DONOR CRUD
# =====================================================

def get_donor_by_phone(db: Session, phone: str):
    return db.query(models.Donor).filter(
        models.Donor.phone == phone
    ).first()


def create_donor(db: Session, donor: schemas.DonorCreate):

    # Phone number must be unique
    existing = get_donor_by_phone(db, donor.phone)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    # Business Rule:
    # Donor cannot donate again within 90 days
    if donor.last_donation_date:
        days = (date.today() - donor.last_donation_date).days

        if days < 90:
            raise HTTPException(
                status_code=400,
                detail="Donor cannot donate again within 90 days"
            )

    db_donor = models.Donor(**donor.model_dump())

    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)

    return db_donor


def get_donors(db: Session, skip=0, limit=10):
    return db.query(models.Donor).offset(skip).limit(limit).all()


def get_donor(db: Session, donor_id: int):
    return db.query(models.Donor).filter(
        models.Donor.id == donor_id
    ).first()


def update_donor(
    db: Session,
    donor_id: int,
    donor: schemas.DonorUpdate
):

    db_donor = get_donor(db, donor_id)

    if not db_donor:
        return None

    update_data = donor.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_donor, key, value)

    db.commit()
    db.refresh(db_donor)

    return db_donor


def delete_donor(db: Session, donor_id: int):

    donor = get_donor(db, donor_id)

    if not donor:
        return None

    db.delete(donor)
    db.commit()

    return donor

# =====================================================
# INVENTORY CRUD
# =====================================================

def create_inventory(
    db: Session,
    inventory: schemas.InventoryCreate
):

    if inventory.expiry_date <= date.today():
        raise HTTPException(
            status_code=400,
            detail="Cannot add expired blood units"
        )

    db_inventory = models.BloodInventory(
        **inventory.model_dump()
    )

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def get_inventory(db: Session):
    return db.query(
        models.BloodInventory
    ).all()


def get_inventory_by_id(
    db: Session,
    inventory_id: int
):
    return db.query(
        models.BloodInventory
    ).filter(
        models.BloodInventory.id == inventory_id
    ).first()


def update_inventory(
    db: Session,
    inventory_id: int,
    inventory: schemas.InventoryUpdate
):

    db_inventory = get_inventory_by_id(
        db,
        inventory_id
    )

    if not db_inventory:
        return None

    update_data = inventory.model_dump(
        exclude_unset=True
    )

    if (
        "expiry_date" in update_data and
        update_data["expiry_date"] <= date.today()
    ):
        raise HTTPException(
            status_code=400,
            detail="Cannot store expired blood units"
        )

    for key, value in update_data.items():
        setattr(
            db_inventory,
            key,
            value
        )

    db.commit()
    db.refresh(db_inventory)

    return db_inventory

# =====================================================
# BLOOD REQUEST CRUD
# =====================================================

def create_request(db: Session, request: schemas.BloodRequestCreate):

    db_request = models.BloodRequest(
        **request.model_dump()
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request


def get_requests(db: Session):
    return db.query(models.BloodRequest).all()


def get_request(db: Session, request_id: int):
    return db.query(models.BloodRequest).filter(
        models.BloodRequest.id == request_id
    ).first()


def update_request(
    db: Session,
    request_id: int,
    request: schemas.BloodRequestUpdate
):

    db_request = get_request(db, request_id)

    if not db_request:
        return None

    # Update normal fields
    update_data = request.model_dump(exclude_unset=True)

    # Business rule when approving
    if update_data.get("status") == "Approved":

        inventory = db.query(models.BloodInventory).filter(
            models.BloodInventory.blood_group == db_request.blood_group
        ).first()

        if inventory is None:
            raise HTTPException(
                status_code=400,
                detail="Blood group not available in inventory"
            )

        if inventory.expiry_date < date.today():
            raise HTTPException(
                status_code=400,
                detail="Expired blood units cannot be allocated"
            )

        if inventory.units_available < db_request.units_required:
            raise HTTPException(
                status_code=400,
                detail="Insufficient blood stock"
            )

        # Automatically reduce inventory
        inventory.units_available -= db_request.units_required

    for key, value in update_data.items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)

    return db_request

# =====================================================
# REPORTS
# =====================================================

def search_donors(
    db: Session,
    blood_group: str = None,
    city: str = None,
    skip: int = 0,
    limit: int = 10
):

    query = db.query(models.Donor)

    if blood_group:
        query = query.filter(
            models.Donor.blood_group == blood_group
        )

    if city:
        query = query.filter(
            models.Donor.city.ilike(f"%{city}%")
        )

    return query.offset(skip).limit(limit).all()


def filter_requests(
    db: Session,
    status: str = None,
    skip: int = 0,
    limit: int = 10
):

    query = db.query(models.BloodRequest)

    if status:
        query = query.filter(
            models.BloodRequest.status == status
        )

    return query.offset(skip).limit(limit).all()


def blood_stock_report(db: Session):
    return db.query(models.BloodInventory).all()

from datetime import timedelta


# =====================================================
# DONATION HISTORY
# =====================================================

def create_donation(
    db: Session,
    donation: schemas.DonationCreate
):

    donor = db.query(models.Donor).filter(
        models.Donor.id == donation.donor_id
    ).first()

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    if donor.last_donation_date:

        days = (
            donation.donation_date -
            donor.last_donation_date
        ).days

        if days < 90:
            raise HTTPException(
                status_code=400,
                detail="Donor cannot donate again within 90 days"
            )

    db_donation = models.DonationHistory(
        **donation.model_dump()
    )

    db.add(db_donation)

    donor.last_donation_date = donation.donation_date
    donor.is_eligible = False

    inventory = db.query(
        models.BloodInventory
    ).filter(
        models.BloodInventory.blood_group == donation.blood_group
    ).first()

    if inventory:

        inventory.units_available += donation.units_donated

    else:

        inventory = models.BloodInventory(
            blood_group=donation.blood_group,
            units_available=donation.units_donated,
            expiry_date=donation.donation_date + timedelta(days=35),
            storage_location="Default Storage"
        )

        db.add(inventory)

    db.commit()
    db.refresh(db_donation)

    return db_donation


def get_my_donations(
    db: Session,
    donor_id: int
):

    return db.query(
        models.DonationHistory
    ).filter(
        models.DonationHistory.donor_id == donor_id
    ).all()