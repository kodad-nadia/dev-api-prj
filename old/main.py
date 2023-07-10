from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

# Connexion DB
connexion = psycopg2.connect(
    host="dpg-ci8rn6dgkuvmfnsaagmg-a.frankfurt-postgres.render.com",
    database="shop_wise",
    user="nadia",
    password="f5yLV6vAF5BNjPe8b1Ok27R97ziKIt5m",
    cursor_factory=RealDictCursor
)
cursor = connexion.cursor()  # TODO Faire des trucs

# description
api_description = """
Shop-Wise API is a comprehensive shopping API that allows users to browse, search, and purchase a wide range of products online. It provides a robust set of endpoints to handle various aspects of the shopping experience, including managing products, user accounts, and orders. 
The API is designed to be intuitive, scalable, and secure, making it an ideal choice for building modern e-commerce applications.
Shop-Wise API is a RESTful API designed for managing a shopping application. 
"""

# Data Models / Schema / DTO
class Clothes(BaseModel):
    clothesType: str
    clothesPrice: float
    featured: bool = True

class Users(BaseModel):
    userName: str
    userAge: int
    userEmail: str

class Orders(BaseModel):
    orderID: int
    clothes: Clothes
    user: Users

app = FastAPI(
    title="Shop-Wise",
    description=api_description
)

@app.get("/", tags=["Clothes"])
async def root():
    return {"message": "Clothes API"}

@app.get("/clothes", tags=["Clothes"])
async def getClothes():
    # requete SQL
    cursor.execute("SELECT * FROM clothe")
    dbClothes = cursor.fetchall()
    return {
        "clothes": dbClothes,
        "limit": 10,
        "total": len(dbClothes),
        "skip": 0
    }

@app.post("/clothes", tags=["Clothes"])
async def create_post(payload: Clothes, response: Response):
    cursor.execute(
        "INSERT INTO clothe (type, price, featured) VALUES (%s,%s,%s) RETURNING *;",
        (payload.clothesType, payload.clothesPrice, payload.featured)
    )
    connexion.commit()  # save in the DB
    response.status_code = status.HTTP_201_CREATED
    return {"message": f"New clothes in store: {payload.clothesType}"}

@app.get("/clothes/{clothes_id}", tags=["Clothes"])
async def get_clothes(clothes_id: int):
    try:
        cursor.execute(f"SELECT * FROM clothe WHERE id={clothes_id}")
        corresponding_clothes = cursor.fetchone()
        if corresponding_clothes:
            return corresponding_clothes
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothes not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothes not found"
        )

@app.delete("/clothes/{clothes_id}", tags=["Clothes"])
async def delete_clothes(clothes_id: int, response: Response):
    try:
        cursor.execute(f"DELETE FROM clothe WHERE id={clothes_id}")
        connexion.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothes not found"
        )

@app.put("/clothes/{clothes_id}", tags=["Clothes"])
async def replace_clothes(clothes_id: int, payload: Clothes, response: Response):
    try:
        cursor.execute(
            "UPDATE clothe SET type=%s, price=%s, featured=%s WHERE id=%s RETURNING *;",
            (payload.clothesType, payload.clothesPrice, payload.featured, clothes_id)
        )
        updated_clothes = cursor.fetchone()
        connexion.commit()
        if updated_clothes:
            return {"message": f"Clothes updated successfully: {payload.clothesType}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothes not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothes not found"
        )

@app.get("/users", tags=["Users"])
async def getUsers():
    cursor.execute("SELECT * FROM users")
    dbUsers = cursor.fetchall()
    return {
        "users": dbUsers,
        "limit": 10,
        "total": len(dbUsers),
        "skip": 0
    }

@app.put("/users/{user_id}", tags=["Users"])
async def update_user(user_id: int, payload: Users, response: Response):
    try:
        cursor.execute(
            "UPDATE users SET name=%s, age=%s, email=%s WHERE id=%s RETURNING *;",
            (payload.userName, payload.userAge, payload.userEmail, user_id)
        )
        updated_user = cursor.fetchone()
        connexion.commit()
        if updated_user:
            return {"message": f"User updated successfully: {payload.userName}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, response: Response):
    try:
        cursor.execute(f"DELETE FROM users WHERE id={user_id}")
        connexion.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@app.put("/orders/{order_id}", tags=["Orders"])
async def update_order(order_id: int, payload: Orders, response: Response):
    try:
        cursor.execute(
            "UPDATE orders SET clothes_id=%s, user_id=%s WHERE id=%s RETURNING *;",
            (payload.clothes.clothesType, payload.user.userName, order_id)
        )
        updated_order = cursor.fetchone()
        connexion.commit()
        if updated_order:
            return {"message": f"Order updated successfully: {payload.orderID}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

@app.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int, response: Response):
    try:
        cursor.execute(f"DELETE FROM orders WHERE id={order_id}")
        connexion.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
