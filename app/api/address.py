from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.depedencies import get_db
from app.models.user import User
from app.schemas.adress import (
    AddressCreate,
    AddressUpdate,
)
from app.schemas.common import ApiResponse
from app.services.address_service import address_service

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)

@router.post(
    "",
    response_model=ApiResponse,
)
def create_address(
    request: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = address_service.create_address(
        db=db,
        request=request,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Address created successfully.",
        data=address,
    )
    
@router.get(
    "",
    response_model=ApiResponse,
)
def get_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    addresses = address_service.get_addresses(
        db=db,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Addresses fetched successfully.",
        data=addresses,
    )
    
@router.get(
    "/{address_id}",
    response_model=ApiResponse,
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = address_service.get_address(
        db=db,
        address_id=address_id,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Address fetched successfully.",
        data=address,
    )
    
@router.put(
    "/{address_id}",
    response_model=ApiResponse,
)
def update_address(
    address_id: int,
    request: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = address_service.update_address(
        db=db,
        address_id=address_id,
        request=request,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Address updated successfully.",
        data=address,
    )

@router.delete(
    "/{address_id}",
    response_model=ApiResponse,
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address_service.delete_address(
        db=db,
        address_id=address_id,
        current_user=current_user,
    )

    return ApiResponse(
        success=True,
        message="Address deleted successfully.",
        data=None,
    )