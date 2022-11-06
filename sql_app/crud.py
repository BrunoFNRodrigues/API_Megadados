from sqlalchemy.orm import Session
from sqlalchemy import delete
from . import models, schemas

def add_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Inventory(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, id_product: int):
    db.query(models.Inventory).filter(models.Inventory.id_product == id_product).delete(synchronize_session="fetch")
    db.commit()
    return {"Product deleted": id_product}

def patch_product(db: Session, id_product: int, new_details: schemas.ProductPatch):
    db.query(models.Inventory).filter(models.Inventory.id_product ==id_product).update(
        **new_details.dict(), synchronize_session="fetch"
    )
    db.commit()
    return get_product(db, id_product)

def add_movement(db: Session, id_product: int, quantity_changed: schemas.ProductQuantity):
    db_quantity = models.Movement(id_product = id_product, movement_quantity = quantity_changed.quantity)
    db.add(db_quantity)

    product = get_product(db, id_product).__dict__
    curr_qty = product['quantity']
    new_qty = curr_qty + quantity_changed.quantity
    if new_qty < 0:
        db.rollback()
        return None

    db.commit()

    patch_quantity_inventory(db, id_product, new_qty)
    #db.commit()
    #db.refresh(db_quantity)
    return get_product(db, id_product)

def patch_quantity_inventory(db: Session, id_product: int, new_quantity: int):
    db.query(models.Inventory).filter(models.Inventory.id_product == id_product).update(
        {"quantity" : new_quantity}, synchronize_session="fetch"
    )
    db.commit()
    return None

def get_product(db: Session, id_product: int):
    return db.query(models.Inventory).filter(models.Inventory.id_product == id_product).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()