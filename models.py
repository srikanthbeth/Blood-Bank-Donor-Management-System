from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ==========================================
# USER TABLE
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    donor = relationship("Donor", back_populates="user", uselist=False)


# ==========================================
# DONOR TABLE
# ==========================================
class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    blood_group = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    last_donation_date = Column(Date, nullable=True)
    is_eligible = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="donor")


# ==========================================
# BLOOD INVENTORY TABLE
# ==========================================
class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id = Column(Integer, primary_key=True, index=True)
    blood_group = Column(String, nullable=False)
    units_available = Column(Integer, default=0)
    expiry_date = Column(Date, nullable=False)
    storage_location = Column(String, nullable=False)


# ==========================================
# BLOOD REQUEST TABLE
# ==========================================
class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    units_required = Column(Integer, nullable=False)
    request_date = Column(Date, nullable=False)
    status = Column(String, default="Pending")

class DonationHistory(Base):
    __tablename__ = "donation_history"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    blood_group = Column(String, nullable=False)
    units_donated = Column(Integer, nullable=False)
    donation_date = Column(Date, nullable=False)

    donor = relationship("Donor")