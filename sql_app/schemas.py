from typing import Union
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    #id: int = Field(ge=0, title= "Product ID", description="ID must be greater than or equal to zero and must not repeat.")
    name: str = Field(title= "Name of the product")
    description: Union[str, None] = Field(
        default=None, title="Description of the product", description="This field is optional", max_length=300
    )
    price: float = Field(gt=0, description="The price of the product. Must be greater than zero.")
    quantity: int = Field(ge=0, description="Quantity in stock. Must be greater than or equal to zero.")

    class Config:
        schema_extra = {
            "example": {
                "name": "Leite",
                "description": "Caixa de leite da empresa X",
                "price": 4.30,
                "quantity": 12,
            }
        }

class Product(ProductCreate):
    id_product: int = Field(ge=0, title= "Product ID", description="ID must be greater than or equal to zero and must not repeat.")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 12,
                "name": "Leite",
                "description": "Caixa de leite da empresa X",
                "price": 4.30,
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
                "price": 52.55,
            }
        }

class ProductQuantity(BaseModel):
    quantity: int = Field(ge=0, description="Quantity in stock. Must be greater than or equal to zero.")
    class Config:
        schema_extra = {
            "example": {
                "quantity": 23.00
            }
        }
