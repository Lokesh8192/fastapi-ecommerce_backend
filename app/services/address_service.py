from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import NotFoundException
from app.models.address import Address
from app.models.user import User
from app.repositories.address_repository import address_repository
from app.schemas.adress import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
)


class AddressService:

    @staticmethod
    def _get_user_address(
        db: Session,
        user_id: int,
        address_id: int,
    ) -> Address:
        address = address_repository.get_by_id(db, address_id)

        if not address or address.user_id != user_id:
            raise NotFoundException("Address not found.")

        return address

    @staticmethod
    def create_address(
        db: Session,
        request: AddressCreate,
        current_user: User,
    ) -> AddressResponse:
        try:
            if request.is_default:
                defaults = address_repository.get_default_addresses(
                    db,
                    current_user.id,
                )

                for address in defaults:
                    address.is_default = False

            address = Address(
                user_id=current_user.id,
                full_name=request.full_name,
                phone_number=request.phone_number,
                address_line1=request.address_line1,
                address_line2=request.address_line2,
                city=request.city,
                state=request.state,
                postal_code=request.postal_code,
                country=request.country,
                landmark=request.landmark,
                is_default=request.is_default,
            )

            address = address_repository.create(db, address)

            db.commit()
            db.refresh(address)

            return AddressResponse.model_validate(address)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_addresses(
        db: Session,
        current_user: User,
    ) -> list[AddressResponse]:

        addresses = address_repository.get_by_user(
            db,
            current_user.id,
        )

        return [
            AddressResponse.model_validate(address)
            for address in addresses
        ]

    @staticmethod
    def get_address(
        db: Session,
        address_id: int,
        current_user: User,
    ) -> AddressResponse:

        address = AddressService._get_user_address(
            db,
            current_user.id,
            address_id,
        )

        return AddressResponse.model_validate(address)

    @staticmethod
    def update_address(
        db: Session,
        address_id: int,
        request: AddressUpdate,
        current_user: User,
    ) -> AddressResponse:

        address = AddressService._get_user_address(
            db,
            current_user.id,
            address_id,
        )

        try:
            if request.is_default:
                defaults = address_repository.get_default_addresses(
                    db,
                    current_user.id,
                )

                for default_address in defaults:
                    default_address.is_default = False

            for field, value in request.model_dump(
                exclude_unset=True
            ).items():
                setattr(address, field, value)

            address = address_repository.update(
                db,
                address,
            )

            db.commit()
            db.refresh(address)

            return AddressResponse.model_validate(address)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_address(
        db: Session,
        address_id: int,
        current_user: User,
    ) -> None:

        address = AddressService._get_user_address(
            db,
            current_user.id,
            address_id,
        )

        try:
            address_repository.delete(
                db,
                address,
            )

            db.commit()

        except Exception:
            db.rollback()
            raise


address_service = AddressService()
