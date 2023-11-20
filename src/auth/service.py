from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from jose import jwt, JWTError, ExpiredSignatureError

from src.hashing_algorithms.service import HashingAlgorithmService
from .models import UserAuth, RefreshToken
from .schemas import UserAuthCreate, UserAuthLogin, UserAuthResponse
from ..config.database import SessionLocal
from ..exceptions import DatabaseOperationException, AlreadyExistsException, NotFoundException, AuthenticationException, TokenExpiredError
from .security import verify_password, create_token, decode_token, is_token_expired
from ..config.settings import settings


class AuthService:
    """Service class for authentication-related operations."""

    @staticmethod
    def create(user_data: UserAuthCreate):
        """Creates a new user."""
        hash_algorithm_id = HashingAlgorithmService.get_hash_algorithm_id("bcrypt")
        if not hash_algorithm_id:
            raise ValueError("Hash algorithm ID could not be determined")

        try:
            with SessionLocal() as db:
                user_data.hash_algorithm_id = hash_algorithm_id

                user = UserAuth(**user_data.dict())
                db.add(user)
                db.commit()
                db.refresh(user)
                response_data = UserAuthResponse(
                    id=user.id,
                    email=user.email,
                    is_email_verified=user.is_email_verified,
                )
                return response_data
        except IntegrityError as exc:
            db.rollback()
            raise AlreadyExistsException(
                f"User with email {user_data.email} already exists.") from exc
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def login(user_data: UserAuthLogin):
        """Authenticates a user and generates a JWT token."""
        try:
            with SessionLocal() as db:
                user = db.query(UserAuth).filter(
                    UserAuth.email == user_data.email).first()
                if not user or not verify_password(user_data.password, user.password):
                    raise AuthenticationException(
                        "Incorrect email or password")

                access_token = create_token(
                    data={"id": user.id}, token_type="access")
                refresh_token = create_token(
                    data={"id": user.id}, token_type="refresh")
                previous_refresh_token = AuthService.get_latest_refresh_token(
                    user.id)
                if previous_refresh_token:
                    AuthService.mark_token_as_used(db, previous_refresh_token)
                AuthService.save_refresh_token(user.id, refresh_token)
                return {"access_token": access_token, "token_type": "bearer"}
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def refresh_token(token: str):
        """Refreshes JWT token."""
        try:
            # Decode the refresh token
            payload = decode_token(token, settings.JWT_SECRET_KEY, [
                                   settings.JWT_ALGORITHM])

            user_id = payload.get("id")
            if user_id is None:
                raise AuthenticationException("User ID not found in token")

            with SessionLocal() as db:
                refresh_token_record = AuthService.get_latest_refresh_token(
                    user_id)

                if is_token_expired(refresh_token_record.token, settings.JWT_REFRESH_TOKEN_SECRET_KEY):
                    raise AuthenticationException(
                        "Authentication failed! Please try again")

                if not refresh_token_record or refresh_token_record.is_used:
                    raise AuthenticationException(
                        "Invalid or used refresh token")

                # Generate new tokens
                access_token = create_token(
                    data={"id": user_id}, token_type="access")
                new_refresh_token = create_token(
                    data={"id": user_id}, token_type="refresh")

                # Save the new refresh token and mark the old one as used
                AuthService.save_refresh_token(user_id, new_refresh_token)
                AuthService.mark_token_as_used(db, refresh_token_record)

                return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

        except ExpiredSignatureError as e:
            raise AuthenticationException("Refresh token expired") from e
        except JWTError as e:
            raise AuthenticationException(f"Token error: {str(e)}") from e
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e
        except Exception as e:
            raise AuthenticationException(f"Unexpected error: {str(e)}") from e

    @staticmethod
    def mark_token_as_used(db, refresh_token_record):
        """Marks a refresh token as used."""
        try:
            refresh_token_record.is_used = True
            db.add(refresh_token_record)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def save_refresh_token(user_id, refresh_token):
        """Saves a refresh token to the database."""
        try:
            with SessionLocal() as db:
                new_refresh_token = RefreshToken(
                    user_id=user_id, token=refresh_token)
                db.add(new_refresh_token)
                db.commit()
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_latest_refresh_token(user_id: int):
        """Fetches the most recently created refresh token for a user."""
        try:
            with SessionLocal() as db:
                latest_refresh_token = db.query(RefreshToken).filter(
                    RefreshToken.user_id == user_id).order_by(
                    RefreshToken.created_at.desc()).first()
                return latest_refresh_token
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_user_from_token(token: str):
        """Fetches a user from a JWT token."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[
                settings.JWT_ALGORITHM])
            user_id = payload.get("id")
            if user_id is None:
                return None

            with SessionLocal() as db:
                user = db.query(UserAuth).filter(
                    UserAuth.id == user_id).first()
                return user
        except ExpiredSignatureError as e:
            raise TokenExpiredError(str("what the fuck!!!")) from e
        except JWTError as e:
            raise AuthenticationException(str(e)) from e
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e
        except Exception as e:
            raise ValueError(str(e)) from e

    @staticmethod
    def get_user_by_email(email: str):
        """Fetches a user by their email."""
        try:
            with SessionLocal() as db:
                user = db.query(UserAuth).filter(
                    UserAuth.email == email).first()
                if not user:
                    raise NotFoundException(
                        f"User with email {email} not found.")
                return user
        except SQLAlchemyError as e:
            # Handling any other database related errors
            raise DatabaseOperationException(str(e)) from e
