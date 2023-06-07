from typing import Optional
from urllib import response
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel

# Data Models / Shema / DTO
class Clothes (BaseModel):
 clothesType : str
 clothesPrice : float # datatypes : http://https://docs.pydantic.dev/latest/
 availability: bool = True # default / optionel
 rating: Optional[int] # Complement optionnel

app = FastAPI() 

@app.get("/")
async def root():
 return {"message": "Hello"}

clothesList = [
 {"clothesType":"dress", "clothesPrice":57},
 {"clothesType":"skirt", "clothesPrice":60}
 ]
 
@app.get("/clothes")
async def getClothes():
 return{
  "clothes": clothesList,
   "limit":10,
   "total":2,
   "skip":0
 }

@app.post("/clothes")
async def create_post(payload: Clothes, response:Response):
  print(payload.clothesType)
  clothesList.append(payload.dict())
  response.status_code = status.HTTP_201_CREATED
  return {"message":f"New clothes in store : {payload.clothesType}"}

@app.get("/clothes/{clothes_id}")
async def get_clothes(clothes_id: int, respnse:Response):
    try:
      corresponding_clothes = clothesList[clothes_id - 1]  # id commence par 1 et tableau commence par 0
      return corresponding_clothes
    except:
      raise HTTPException(
      status.HTTP_404_NOT_FOUND,
      detail="Clothes not found"
      )

