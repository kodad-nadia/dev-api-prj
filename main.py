from fastapi import FastAPI
app = FastAPI() 

@app.get("/clothes")
async def get_clothes():
  
 clothes = ["shirt jane","pants","dress amber","skirt jolen"]
 return clothes