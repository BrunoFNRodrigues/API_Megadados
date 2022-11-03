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
    return 'Deleted'

def patch_product(db: Session, id_product: int, new_details: schemas.ProductPatch):
    db.query(models.Inventory).filter(models.Inventory.id_product ==id_product).update(
        **new_details.dict(), synchronize_session="fetch"
    )
    db.commit()
    return 'Updated'

def alter_quantity(db: Session, id_product: int, quantity_changed: int):
    db_quantity = models.Movement(id_product = id_product, movement_quantity = quantity_changed)
    db.add(db_quantity)
    db.commit()
    db.refresh(db_quantity)
    return db_quantity


###Ainda mudar valores na tabela de estoque