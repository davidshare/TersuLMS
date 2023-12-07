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
    
def update_order(model, order_column, parent_column, parent_id, updates, session):
    """
    Updates the ordering of items within a specific parent entity.

    Args:
        model: The database model to reorder.
        order_column: The column used for ordering.
        parent_column: The column that refers to the parent entity.
        parent_id: The ID of the parent entity.
        updates: A list of tuples with item IDs and their new order.
        session: The database session to use.
    """
    try:
        items = session.query(model).filter(getattr(model, parent_column) == parent_id).all()
        item_dict = {getattr(item, 'id'): item for item in items}

        for item_id, new_order in updates:
            item = item_dict.get(item_id)
            if item:
                setattr(item, order_column.name, new_order)
                session.add(item)

            session.commit()
    except SQLAlchemyError as e:
        logger.error(e)
        session.rollback()
        raise e


