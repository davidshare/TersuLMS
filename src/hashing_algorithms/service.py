from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.config.database import SessionLocal
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from src.hashing_algorithms.model import HashingAlgorithm


class HashingAlgorithmService:
    """Handles hashing algorithm operations."""

    @staticmethod
    def create_hashing_algorithm(algorithm_name: str):
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
