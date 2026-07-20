from fastapi import Depends, HTTPException, status

from oauth2 import get_current_user


def admin_only(current_user=Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def staff_only(current_user=Depends(get_current_user)):
    if current_user.role not in ["Admin", "Staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required"
        )
    return current_user


def donor_only(current_user=Depends(get_current_user)):
    if current_user.role != "Donor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Donor access required"
        )
    return current_user