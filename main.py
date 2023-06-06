from fastapi import FastAPI
app = FastAPI() #variable names for the servers

@app.get("/")


class ClothingItem:
    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.color = color

# Creating clothing items
item1 = ClothingItem("T-shirt", 20.99, "Blue")
item2 = ClothingItem("Jeans", 49.99, "Black")
item3 = ClothingItem("Dress", 39.99, "Red")

# Creating a list of clothing items
clothes_list = [item1, item2, item3]

# Accessing and printing information about each item in the list
for item in clothes_list:
    print(f"Name: {item.name}")
    print(f"Price: {item.price}")
    print(f"Color: {item.color}")
    print("---")

