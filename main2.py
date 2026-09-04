from typing import Dict

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class ItemBase(BaseModel):
    name: str
    price: float


class Item(ItemBase):
    id: int


items_db: Dict[int, Item] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items", response_model=list[Item])
def list_items():
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemBase):
    global next_id

    new_item = Item(id=next_id, name=item.name, price=item.price)
    items_db[next_id] = new_item
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemBase):
    existing_item = items_db.get(item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = Item(id=item_id, name=item.name, price=item.price)
    items_db[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": "Item deleted"}



