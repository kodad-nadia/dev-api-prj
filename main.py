from fastapi import FastAPI
app = FastAPI() #variable names for the servers

@app.get("clothes")
async def root():
      return{"shirt jane","pants","dress amber","skirt jolen"}

