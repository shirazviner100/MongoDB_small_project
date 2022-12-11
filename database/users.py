from database.database import users_col, products_col
from bson import ObjectId, errors


class UserNotFoundException(Exception):
    pass

def user_helper(user: dict) -> dict:
    return {
        "obj_id": str(user['_id']),
        "email": user['email'],
        "first_name": user['first_name'],
        "last_name": user['last_name'],
        "city": user["city"],
        "address": user["address"],
        "phone": user['phone'],
        "status": user['status'], #user is buyer or seller
        "orders": user['orders']
    }

#------------------- FUNCTIONALITY ------------------#

def insert_user(user: dict) -> dict:
    new_user = users_col.insert_one(user)
    return str(new_user.inserted_id)


def retrieve_user(email: str):
    try:
        user = users_col.find_one({"email": email})
        if user:
            return user_helper(user)
        else:
            raise UserNotFoundException(f"Could not find user by email: {email}")
    except errors.InvalidId as ex:
        raise ex


def delete_user(user_id: str):
    try:
        find_user = users_col.find_one({"_id": ObjectId(str(user_id))})

        if find_user:
            #if the user is seller we need to delete his products 
            if find_user['status'] == 'seller':
                remove_products_by_seller_id(find_user['_id'])

            users_col.delete_one(find_user)
                
        else:
            raise UserNotFoundException(f'Could not delte user id: {user_id}')
    except errors.InvalidId as ex:
        raise ex


def remove_products_by_seller_id(seller_id: str):
    products_list = products_col.find({"seller_id": seller_id})
    for product in products_list:
        products_col.delete_one({"_id": product["_id"]})


def update_user(user_id: str, data: dict):
    if "_id" in data:
        data.pop("_id")

    try:
        find_user = users_col.find_one({"_id": ObjectId(user_id)})
        if find_user:
            for key in data.keys():
                #user moves his status from seller to buyer so his products unavliable
                if key == 'status' and find_user['status'] == 'seller' and data[key] == 'buyer':
                    remove_products_by_seller_id(find_user['_id'])

                if data[key]:
                    find_user[key] = data[key]
            
            users_col.update_one({"_id": find_user["_id"]}, {"$set": find_user})
        else:
            raise UserNotFoundException(f'Could not find user by id: {user_id}')
    
    except errors.InvalidId as ex:
        raise ex