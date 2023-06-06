from fastapi import FastAPI
app = FastAPI() #variable names for the servers


# List of clothing items
clothes = [
    {"name": "shirt jane", "type": "shirt", "color": "Blue", "price": 20.99},
    {"name": "pants", "type": "trousers", "color": "Black", "price": 49.99},
    {"name": "dress amber", "type": "dress", "color": "Red", "price": 39.99},
    {"name": "skirt jolen", "type": "skirt", "color": "Yellow", "price": 29.99},
]

@app.get("/clothes")
async def get_clothes():
    return {"clothes": clothes}