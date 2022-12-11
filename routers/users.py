from fastapi import Body, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from database.users import insert_user, retrieve_user, update_user, delete_user, UserNotFoundException
from bson import objectid, errors
from modules.users import ResponseModel, UserModel, UpdateUserModel
from database.database import users_col

router = APIRouter()


@router.get("/get_user/{email}")
async def get_user(email):
    try:
        user = retrieve_user(email)
        return ResponseModel(user, "User data found succesfully.")
    except UserNotFoundException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.post("/add_user")
async def add_user(user: UserModel = Body(...)):
    user_exists = users_col.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=404, detail="Email already exist in the system")
    else:
        new_user = insert_user(jsonable_encoder(user))
        return new_user
        return ResponseModel(new_user, "User added succesfully")



@router.patch("/update_user/{user_id}")
async def update_user_detailes(user_id: str, user: UpdateUserModel = Body(...)):
    try:
        update_user(user_id, jsonable_encoder(user))
        return ResponseModel(f"User id {user_id} updated succefuly", "User Updated")

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User doesn't exist.")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/delete_user/{user_id}")
async def remove_user(user_id: str):
    try:
        delete_user(user_id)
        return ResponseModel(f"User by id {user_id} deleted succesfuly", "Deleted complite")

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User was not found")
    except errors.InvalidId as ex:
        raise HTTPException(status_code=404, detail=str(ex))
