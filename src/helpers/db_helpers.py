from sqlalchemy.exc import SQLAlchemyError

from src.exceptions import DatabaseOperationException
from ..logger import logger


def reorder_items(model, filter_condition, session):
    """
    Reorders items in a database model to ensure sequential ordering after update or deletion.

    Args:
        model: The database model class.
        filter_condition: The condition to filter the items that need reordering.
        session: The database session.
    """
    try:
        items = session.query(model).filter(filter_condition).order_by(model.ordering).all()

        expected_order = 1
        for item in items:
            if item.ordering != expected_order:
                item.ordering = expected_order
                session.add(item)  # Mark for update
            expected_order += 1

        session.commit()
    except SQLAlchemyError as e:
        logger.error(e)
        session.rollback()
        raise DatabaseOperationException(str(e)) from e

