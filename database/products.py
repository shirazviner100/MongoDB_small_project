from database.database import products_col
from bson import ObjectId, errors
from database.users import users_col, UserNotFoundException

def product_helper(product: dict) -> dict:
    return {
        "obj_id": str(product['_id']),
        "name": product['name'],
        "title": product['title'],
        "color": product['color'],
        "price": product['price'],
        "tags": product['tags'],
        "seller_id": product['seller_id']
    }

class UserTypeException(Exception):
    pass

class ProductNotFoundException(Exception):
    pass

#------------------- FUNCTIONALITY ------------------#


def find_by_seller(seller_id: str) -> list: 
    try:
        seller = users_col.find_one({"_id": ObjectId(seller_id)})
        if seller:
            if seller["status"] == "seller":
                seller_products = []
                for product in products_col.find({"seller_id": seller_id}):
                    seller_products.append(product_helper(product))

                return seller_products
            
            else:
                raise UserTypeException(f"User id {seller_id} not matching to seller status")
        else:
            raise UserNotFoundException(f"User id - {seller_id} not found")

    except errors.InvalidId as ex:
        raise ex


def insert_product(product: dict) -> str:
    try:
        seller = users_col.find_one({"_id": ObjectId(product["seller_id"])})
        if seller:
            if seller["status"] == "seller":
                new_product = products_col.insert_one(product)
                return str(new_product.inserted_id)
            else:
                raise UserTypeException(f"User not seller")
        else:
            raise UserNotFoundException("user id not found")
    except errors.InvalidId as ex:
        raise ex


def delete_product(product_id: str):
    try:
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if product:
            products_col.delete_one(product)
        else:
            raise ProductNotFoundException(f'Could not delte product id {product_id}')

    except errors.InvalidId as ex:
        raise ex


def update_product(product_id: str, data: dict) -> dict:
    try:
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if product:
            if "_id" in data:
                data.pop("_id")

            for key in data.keys():
                if data[key]:
                    product[key] = data[key]

            products_col.update_one({"_id": product["_id"]}, {"$set": product})
        
        else:
            raise ProductNotFoundException(f'Could not update product id: {product_id}')
    
    except errors.InvalidId as ex:
        raise ex


def get_product(product_id: str) -> dict:
    try:
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if product:
            return product_helper(product)
        else:
            raise ProductNotFoundException(f"Product id not exists")

    except errors.InvalidId as ex:
        raise ex

