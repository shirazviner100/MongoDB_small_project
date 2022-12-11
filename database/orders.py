from database.database import orders_col, users_col
from bson import ObjectId, errors
from database.products import products_col, ProductNotFoundException, product_helper
from datetime import datetime, timedelta
from database.users import UserNotFoundException, update_user

def order_helper(order: dict) -> dict:
    return {
        "obj_id": str(order['_id']),
        "total_price": order['total_price'],
        "products": order['products'],
        "date": order['date'],
        "buyer_id": order['buyer_id']
    }


class OrderNotFoundException(Exception):
    pass

class DatePassException(Exception):
    pass


#------------------- FUNCTIONALITY ------------------#

def find_by_user(user_id: str) -> list:
    orders = []
    for order in orders_col.find({"buyer_id": user_id}):
        orders.append(order_helper(order))

    return orders


def insert_order(order: dict) -> str:
    try:
        user = users_col.find_one({"_id": ObjectId(order["buyer_id"])})
        if user:
            if not check_products_id(order["products"]):
                raise ProductNotFoundException("Some products id don`t match to products object")
            else:
                new_order = orders_col.insert_one(order)
                user["orders"].append(str(new_order.inserted_id))
                update_user(order["buyer_id"], user)
                return str(new_order.inserted_id)

        else:
            raise UserNotFoundException("Could not find user id: {}".format(order["buyer_id"]))

    except errors.InvalidId as ex:
        raise ex



def check_products_id(products: list) -> bool:
    for product in products:
        current = products_col.find({"_id": ObjectId(product)}) 
        if current is None:
            return False

    return True


def cancel_order(order_id: str):
    try:
        order = orders_col.find_one({"_id": ObjectId(order_id)})
        if order:
            user = users_col.find_one({"_id": ObjectId(order["buyer_id"])})
            if user:
                order_date = order["date"].split('T')
                date = datetime.strptime(order_date[0], '%Y-%m-%d')
                if (date + timedelta(weeks=2)) > datetime.now():
                    user["orders"].remove(order_id)
                    update_user(order["buyer_id"], user)
                    orders_col.delete_one(order)

                else:
                    raise DatePassException(f'Could not cancle order after 14 days')
            
            else:
                raise UserNotFoundException("Buyer {} was not found".format(order["buyer_id"]))

        else:
            OrderNotFoundException(f'Order {order_id} was not found')

    except errors.InvalidId as ex:
        raise ex


def get_list_of_products_by_order(order_id: str) -> dict:
    try:
        order = orders_col.find_one({"_id": ObjectId(order_id)})
        if order:
            all_products_dict = []
            for product in order["products"]:
                current_product = product_helper(products_col.find_one({"_id": ObjectId(product)}))
                if current_product:
                    all_products_dict.append(current_product)
                else:
                    all_products_dict.append("Product - {} as been deleted from DB".format(current_product["name"]))

            return all_products_dict

        else:
            raise OrderNotFoundException(f"Order id {order_id} not foound")

    except errors.InvalidId as ex:
        raise ex
