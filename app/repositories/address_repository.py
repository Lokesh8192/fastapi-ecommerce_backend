from sqlalchemy.orm import Session

from app.models.address import Address


class AddressRepository:

    @staticmethod
    def create(
        db: Session,
        address: Address,
    ) -> Address:
        db.add(address)
        db.flush()
        db.refresh(address)
        return address

    @staticmethod
    def get_by_id(
        db: Session,
        address_id: int,
    ) -> Address | None:
        return (
            db.query(Address)
            .filter(Address.id == address_id)
            .first()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ) -> list[Address]:
        return (
            db.query(Address)
            .filter(Address.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_default_addresses(
        db: Session,
        user_id: int,
    ) -> list[Address]:
        return (
            db.query(Address)
            .filter(
                Address.user_id == user_id,
                Address.is_default.is_(True),
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        address: Address,
    ) -> Address:
        db.flush()
        db.refresh(address)
        return address

    @staticmethod
    def delete(
        db: Session,
        address: Address,
    ) -> None:
        db.delete(address)
        db.flush()


address_repository = AddressRepository()
