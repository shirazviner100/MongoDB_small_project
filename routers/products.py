from fastapi import Body, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from database.products import insert_product, delete_product, update_product, find_by_seller, ProductNotFoundException, UserTypeException
from database.users import UserNotFoundException
from bson import errors
from modules.products import ProductModel, UpdateProductModel, ResponseModel

router = APIRouter()

@router.get("/products_by_seller/{seller_id}")
async def get_products_by_seller(seller_id: str):
    try:
        return find_by_seller(seller_id)
    except UserTypeException:
        raise HTTPException(status_code=404, detail= "User is not a seller id")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User id {} was not found".format(seller_id))
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.post("/add_product")
async def add_product(product: ProductModel = Body(...)):
    try:
        return insert_product(jsonable_encoder(product))
    except UserTypeException:
        raise HTTPException(status_code=404, detail= "User is not a seller id")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User id {} was not found".format(product.seller_id))
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.patch("/update_product/{product_id}")
async def update_product_details(product_id: str, product: UpdateProductModel= Body(...)):
    try:
        update_product(product_id, product.dict())
        return ResponseModel(f"Product id {product_id} as been updated succefuly", "Updated succefuly")
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail=f"product id {product_id} was not found")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/delete_product/{product_id}")
async def remove_product(product_id: str):
    try:
        delete_product(product_id)
        return ResponseModel(f"Product id - {product_id} deleted succefully", "Delete complite")
    except ProductNotFoundException:
        raise HTTPException(status_code=404, detail=f"Product {product_id} was not found")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))





