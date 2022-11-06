from typing import List

from fastapi import FastAPI, HTTPException, Body, Path, Depends
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

fake_db = {}
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.ProductCreate, summary="Create a product", tags=["Create"])
async def create_product(product: schemas.ProductCreate= Body(
                            example={
                                "name": "Leite",
                                "description": "Caixa de leite da empresa X",
                                "price": 4.3,
                                "quantity": 12,
                            }),
                         db: Session = Depends(get_db)):
    """
    Create a product with all the information:

    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    - **quantity**: quantity in stock
    """
    
    # if product.id in fake_db:
    #     raise HTTPException(
    #         status_code=409,
    #         detail="Conflict in ID. Already exists.",
    #     )
    #fake_db[product.id] = (jsonable_encoder(product))
    return crud.add_product(db=db, product= product)


@app.get("/products/{id_product}", response_model=schemas.Product, summary="Get product information by ID", tags=["Read"])
async def read_product(id_product:int = Path(title="The ID of the product to get",  ge=0), db: Session = Depends(get_db)):
    """
    Get product information by ID:

    - **id**: each product must have a unique ID
    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    - **quantity**: quantity in stock
    """
    db_product = crud.get_product(db, id_product = id_product)

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    return db_product


@app.get("/products/", summary="Get information of all products in stock", tags=["Read"], response_model = List[schemas.Product])
async def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns the details of the first 100 products in stock (by id)
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.patch("/products/{id_product}", response_model=schemas.Product, summary="Updates product details by ID", tags=["Update"])
async def update_product(id_product:int = Path(title="The ID of the product to get",  ge=0), 
                       new_product_details: schemas.ProductPatch = Body(
                                example={
                                    "name": "Novo nome",
                                    "description": "Nova descrição",
                                    "price": 27.89,
                                }),
                        db: Session = Depends(get_db)):
    """
    Updates details about product given it's ID. Can only update:

    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    """
    db_product = crud.get_product(db, id_product = id_product)

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return crud.patch_product(db, id_product, new_product_details)

@app.patch("/products/{id_product}/stock", response_model=schemas.Product, summary="Updates quantity in stock", tags=["Update"])
async def update_quantity(id_product:int = Path(title="The ID of the product to get",  ge=0), 
                        product_mov: schemas.ProductQuantity = Body(
                                example={
                                    "quantity": -23,
                                }),
                        db: Session = Depends(get_db)):
    """
    Updates the quantity of given product ID in stock.
    """
    db_product = crud.get_product(db, id_product = id_product)

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    db_movement = crud.add_movement(db, id_product, product_mov)
    if db_movement is None:
        raise HTTPException(
            status_code=403,
            detail="Invalid inventory movimentation",
        )
    return db_movement

@app.delete("/products/{id_product}", summary="Deletes product", tags=["Delete"])
async def remove_product(id_product:int = Path(title="The ID of the product to get",  ge=0), db: Session = Depends(get_db)):
    """
    Deletes the product given it's ID
    """
    db_product = crud.get_product(db, id_product = id_product)
    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return crud.delete_product(db, id_product)