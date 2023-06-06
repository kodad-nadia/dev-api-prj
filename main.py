from fastapi import FastAPI
app = FastAPI() #variable names for the servers

@app.get("/")
async def root():
      return{"message":"coucou"}