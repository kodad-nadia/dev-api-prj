from fastapi import FastAPI
app = FastAPI() #variable names for the servers

@app.get("/clothes")
async def get_clothes():
  
 clothes = ["shirt jane","pants","dress amber","skirt jolen"]
 return clothes