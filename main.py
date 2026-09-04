from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

import json

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=FileResponse)
def read_root():
    return BASE_DIR / "index.html"


class ItemBase(BaseModel):
    name: str
    contents: str
    status: bool = False # Default value for status


class Item(ItemBase):
    id: int


items_db: Dict[int, Item] = {}
next_id = 1
if Path("save.json").exists():
    with open("save.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
        for k, v in loaded_data.items():
            item = Item(id=v["id"], name=v["name"], contents=v["contents"], status=v["status"])
            items_db[int(k)] = item
    next_id = max(items_db.keys(), default=0) + 1
else:
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

def save_to_json():
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump({k: v.model_dump() for k, v in items_db.items()}, f, ensure_ascii=False, indent=4)

@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: ItemBase):
    global next_id

    new_item = Item(id=next_id, name=item.name, contents=item.contents, status=item.status)
    items_db[next_id] = new_item
    next_id += 1
    save_to_json()
    return new_item

@app.put("/items/item_status/{item_id}", response_model=Item)
def update_item_status(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = Item(id=item_id, name=item.name, contents=item.contents, status=not item.status)
    items_db[item_id] = updated_item
    save_to_json()
    return updated_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemBase):
    existing_item = items_db.get(item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = Item(id=item_id, name=item.name, contents=item.contents, status=item.status)
    items_db[item_id] = updated_item
    save_to_json()
    return updated_item

@app.get("/items/status", response_model=list[Item])
def get_items_by_status(status: bool):
    return [item for item in items_db.values() if item.status == status]

@app.get("/items/item_amount")
def get_item_amount():
    return {"message": len(items_db)}


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items", response_model=list[Item])
def list_items():

    return list(items_db.values()   )

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    save_to_json()
    return {"message": "Item deleted"} 