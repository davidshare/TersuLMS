from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models import UserAuth, HashingAlgorithm
from .schemas import HashingAlgorithmCreate, UserAuthSave
from ..config.database import SessionLocal
from ..exceptions import DatabaseOperationException, AlreadyExistsException, NotFoundException


class AuthService:
    """Service class for authentication-related operations."""
    @staticmethod
    def create(user_data: UserAuthSave):
        """Creates a new user."""
        try:
            with SessionLocal() as db:
                user = UserAuth(**user_data.dict())
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
        except IntegrityError as exc:
            raise AlreadyExistsException(
                f"User with email {user_data.email} already exists.") from exc
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_user_by_email(email: str):
        """Fetches a user by their email."""
        try:
            with SessionLocal() as db:
                user = db.query(UserAuth).filter(UserAuth.email == email).first()
                if not user:
                    raise NotFoundException(f"User with email {email} not found.")
                return user
        except SQLAlchemyError as e:
            # Handling any other database related errors
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def create_hashing_algorithm(algorithm_name: HashingAlgorithmCreate):
        """Creates a new hashing algorithm."""
        try:
            with SessionLocal() as db:
                hashing_algorithm = HashingAlgorithm(**algorithm_name.dict())
                db.add(hashing_algorithm)
                db.commit()
                db.refresh(hashing_algorithm)
                return hashing_algorithm
        except IntegrityError as exc:
            raise AlreadyExistsException(
                f"Hashing algorithm {algorithm_name.algorithm_name} already exists.") from exc
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_hash_algorithm_id(algorithm_name: str):
        """Fetches the ID of a hashing algorithm by its name."""
        try:
            with SessionLocal() as db:
                algorithm = db.query(HashingAlgorithm).filter_by(
                    algorithm_name=algorithm_name).first()
                if not algorithm:
                    raise NotFoundException("Hashing algorithm not found")
                return algorithm.id
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_all_hashing_algorithms():
        """Returns all hashing algorithms."""
        try:
            with SessionLocal() as db:
                return db.query(HashingAlgorithm).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e))from e

    @staticmethod
    def get_hashing_algorithm_by_id(algorithm_id: int):
        """Returns a hashing algorithm based on its ID."""
        try:
            with SessionLocal() as db:
                algorithm = db.query(HashingAlgorithm).filter(
                    HashingAlgorithm.id == algorithm_id).first()
                if not algorithm:
                    raise NotFoundException("Hashing algorithm not found")
                return algorithm
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def get_hashing_algorithm_by_name(algorithm_name: str):
        """Returns a hashing algorithm based on its name."""
        try:
            with SessionLocal() as db:
                algorithm = db.query(HashingAlgorithm).filter(
                    HashingAlgorithm.algorithm_name == algorithm_name).first()
                if not algorithm:
                    raise NotFoundException("Hashing algorithm not found")
                return algorithm
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def update_hashing_algorithm(algorithm_id: int, algorithm_name: str):
        """Updates a hashing algorithm's name."""
        try:
            with SessionLocal() as db:
                algorithm = db.query(HashingAlgorithm).filter(
                    HashingAlgorithm.id == algorithm_id).first()
                if algorithm:
                    algorithm.algorithm_name = algorithm_name
                    db.commit()
                    return algorithm
                else:
                    raise NotFoundException("Hashing algorithm not found")
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e

    @staticmethod
    def delete_hashing_algorithm(algorithm_id: int):
        """Deletes a hashing algorithm."""
        try:
            with SessionLocal() as db:
                algorithm = db.query(HashingAlgorithm).filter(
                    HashingAlgorithm.id == algorithm_id).first()
                if algorithm:
                    db.delete(algorithm)
                    db.commit()
                    return True
                else:
                    raise NotFoundException("Hashing algorithm not found")
        except SQLAlchemyError as e:
            raise DatabaseOperationException(str(e)) from e
