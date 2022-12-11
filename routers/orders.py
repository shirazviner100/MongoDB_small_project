from fastapi import Body, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from bson import errors
from modules.orders import OrderModel, ResponseModel
from database.users import UserNotFoundException
from database.products import ProductNotFoundException
from database.orders import get_list_of_products_by_order, insert_order, cancel_order, find_by_user, DatePassException, OrderNotFoundException

router = APIRouter()


@router.get("/get_user_orders/{user_id}")
async def get_user_orders(user_id: str):
    return find_by_user(user_id)


@router.post("/add_order")
def add_order(order: OrderModel = Body(...)):
    try:
        return insert_order(jsonable_encoder(order))
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Buyer id not found in DB")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/cancel_order/{order_id}")
def remove_order(order_id: str):
    try:
        cancel_order(order_id)
        return ResponseModel("Order {} was cancel".format(order_id), "Cancel success")

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Buyer id invalid")
    except OrderNotFoundException:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    except DatePassException:
        raise HTTPException(status_code=404, detail="Order can`t be cancel - date pass 14 days")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))



@router.get("/get_products_by_order/{order_id}")
def get_products_by_order(order_id: str):
    try:
        return get_list_of_products_by_order(order_id)
    except ProductNotFoundException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except OrderNotFoundException:
        raise HTTPException(status_code=404, detail=f"Order id {order_id} was not found")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))
