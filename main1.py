from typing import Dict

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class ItemBase(BaseModel):
    author: str
    title: str
    publisher: str


class Item(ItemBase):
    id: int
    


items_db: Dict[int, Item] = {}
next_id = 1

@app.get("/items", response_model=list[Item])
def list_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemBase):
    global next_id
    item = Item(id=next_id, author = item.author, title = item.title, publisher = item.publisher)
    items_db[item.id] = item
    next_id += 1
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemBase):
    existing_item = items_db.get(item_id)
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updated_item = Item(id=item_id, author = item.author, title = item.title, publisher = item.publisher)
    items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}

@app.get("/items_by_author/{item_author}", response_model=list[Item])
def get_items_by_author(item_author: str):
    items = [item for item in items_db.values() if item.author == item_author]
    return items

