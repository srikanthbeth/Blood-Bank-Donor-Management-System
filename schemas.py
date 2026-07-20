from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


# =====================================================
# AUTH SCHEMAS
# =====================================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =====================================================
# DONOR SCHEMAS
# =====================================================

class DonorBase(BaseModel):
    name: str
    age: int = Field(..., ge=18, le=65)
    blood_group: str
    phone: str
    city: str
    last_donation_date: Optional[date] = None
    is_eligible: bool = True


class DonorCreate(DonorBase):
    user_id: Optional[int] = None


class DonorUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=65)
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    last_donation_date: Optional[date] = None
    is_eligible: Optional[bool] = None


class DonorResponse(DonorBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True


# =====================================================
# INVENTORY SCHEMAS
# =====================================================

class InventoryBase(BaseModel):
    blood_group: str
    units_available: int = Field(..., ge=0)
    expiry_date: date
    storage_location: str


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    blood_group: Optional[str] = None
    units_available: Optional[int] = Field(None, ge=0)
    expiry_date: Optional[date] = None
    storage_location: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# BLOOD REQUEST SCHEMAS
# =====================================================

class BloodRequestBase(BaseModel):
    hospital_name: str
    blood_group: str
    units_required: int = Field(..., gt=0)
    request_date: date
    status: str = "Pending"


class BloodRequestCreate(BloodRequestBase):
    pass


class BloodRequestUpdate(BaseModel):
    hospital_name: Optional[str] = None
    blood_group: Optional[str] = None
    units_required: Optional[int] = Field(None, gt=0)
    request_date: Optional[date] = None
    status: Optional[str] = None


class BloodRequestResponse(BloodRequestBase):
    id: int

    class Config:
        from_attributes = True

        # =====================================================
# DONATION HISTORY
# =====================================================

class DonationCreate(BaseModel):
    donor_id: int
    blood_group: str
    units_donated: int = Field(..., gt=0)
    donation_date: date


class DonationResponse(DonationCreate):
    id: int

    class Config:
        from_attributes = True