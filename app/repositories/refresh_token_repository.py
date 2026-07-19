from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken


class RefreshTokenRepository():
    @staticmethod
    def create(
        db: Session, refresh_token: RefreshToken,
    ) -> RefreshToken:
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)

        return refresh_token

    @staticmethod
    def get_token(db: Session, token: str,) -> RefreshToken | None:
        return (db.query(RefreshToken)
                .filter(RefreshToken.token == token)
                .first()
                )

    @staticmethod
    def delete(
        db: Session, refresh_token: RefreshToken,
    ) -> None:
        db.delete(refresh_token)
        db.commit()

    @staticmethod
    def delete_by_user(db: Session, user_id: int) -> None:
        (
            db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id)
            .delete()
        )

        db.commit()

    @staticmethod
    def delete_by_user_id(db: Session, user_id: int) -> None:
        (
            db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id)
            .delete(synchronize_session=False)
        )
        db.commit()
