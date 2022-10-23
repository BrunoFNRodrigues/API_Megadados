from tkinter import RADIOBUTTON
from typing import Union

from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

class Product(BaseModel):
    id: int = Field(ge=0, title= "Product ID", description="ID must be greater than or equal to zero and must not repeat.")
    name: str = Field(title= "Name of the product")
    description: Union[str, None] = Field(
        default=None, title="Description of the product", description="This field is optional", max_length=300
    )
    price: float = Field(gt=0, description="The price of the product. Must be greater than zero.")
    quantity: int = Field(ge=0, description="Quantity in stock. Must be greater than or equal to zero.")

    class Config:
        schema_extra = {
            "example": {
                "id": 12,
                "name": "Leite",
                "description": "Caixa de leite da empresa X",
                "price": 4.3,
                "quantity": 12,
            }
        }


class ProductPatch(BaseModel):
    name: str = Field(title= "Name of the product")
    description:  Union[str, None] = Field(
        default=None, title="Description of the product", description="This field is optional", max_length=300
    )
    price: float = Field(gt=0, description="The price of the product. Must be greater than zero.")

    class Config:
        schema_extra = {
            "example": {
                "name": "Novo nome",
                "description": "Nova descricao",
                "price": 52,
            }
        }

class ProductQuantity(BaseModel):
    quantity: int = Field(ge=0, description="Quantity in stock. Must be greater than or equal to zero.")
    class Config:
        schema_extra = {
            "example": {
                "quantity": 23
            }
        }


fake_db = {}

app = FastAPI()

@app.post("/products/", response_model=Product, summary="Create a product", tags=["Create"])
async def create_product(product: Product= Body(
                        example={
                            "id": 12,
                            "name": "Leite",
                            "description": "Caixa de leite da empresa X",
                            "price": 4.3,
                            "quantity": 12,
                        })):
    """
    Create a product with all the information:

    - **id**: each product must have a unique ID
    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    - **quantity**: quantity in stock
    """
    if product.id in fake_db:
        raise HTTPException(
            status_code=409,
            detail="Conflict in ID. Already exists.",
        )
    fake_db[product.id] = (jsonable_encoder(product))
    return product


@app.get("/products/{id_product}", response_model=Product, summary="Get product information by ID", tags=["Read"])
async def read_product(id_product:int = Path(title="The ID of the product to get",  ge=0)):
    """
    Get product information by ID:

    - **id**: each product must have a unique ID
    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    - **quantity**: quantity in stock
    """
    if id_product not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    return fake_db[id_product]


@app.get("/products/", summary="Get information of all products in stock", tags=["Read"])
async def read_all_products():
    """
    Returns the details of all products in stock
    """
    return fake_db



@app.patch("/products/{id_product}", response_model=Product, summary="Updates product details by ID", tags=["Update"])
async def edit_product(id_product:int = Path(title="The ID of the product to get",  ge=0), 
                       product: ProductPatch = Body(
                                example={
                                    "name": "Novo nome",
                                    "description": "Nova descrição",
                                    "price": 27.89,
                                })):
    """
    Updates details about product given it's ID. Can only update:

    - **name**: each product must have a name
    - **description**: description of the product. Optional
    - **price**: price of the product
    """
    
    if id_product not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    stored_product_data = fake_db[id_product]
    stored_product_model = Product(**stored_product_data)
    update_data = product.dict(exclude_unset=True)
    updated_item = stored_product_model.copy(update=update_data)
    fake_db[id_product] = jsonable_encoder(updated_item)
    return updated_item

@app.patch("/products/{id_product}/stock", response_model=Product, summary="Updates quantity in stock", tags=["Update"])
async def edit_quantity(id_product:int = Path(title="The ID of the product to get",  ge=0), 
                       product: ProductQuantity = Body(
                                example={
                                    "quantity": 23,
                                })):
    """
    Updates the quantity of given product ID in stock.
    """
    
    if id_product not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    stored_product_data = fake_db[id_product]
    stored_product_model = Product(**stored_product_data)
    update_data = product.dict(exclude_unset=True)
    updated_item = stored_product_model.copy(update=update_data)
    fake_db[id_product] = jsonable_encoder(updated_item)
    return updated_item

@app.delete("/products/{id_product}", summary="Deletes product", tags=["Delete"])
async def remove_product(id_product:int = Path(title="The ID of the product to get",  ge=0)):
    """
    Deletes the product given it's ID
    """
    if id_product not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    fake_db.pop(id_product)
    return {"Product deleted": id_product}