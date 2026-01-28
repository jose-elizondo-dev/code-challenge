from fastapi import Depends, FastAPI, Header, Query, HTTPException
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
from datetime import datetime, timezone
from app.settings import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI App",
    version="0.1.0",
)

security = HTTPBearer()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---

Category = Literal["main", "side", "drink", "dessert"]
SortField = Literal["price", "name"]
SortOrder = Literal["asc", "desc"]


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    category: Category
    price: float
    isAvailable: bool = True

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str):
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[Category] = None
    price: Optional[float] = None
    isAvailable: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip() if v else v


class Item(BaseModel):
    id: str
    name: str
    category: Category
    price: float
    isAvailable: bool = True
    isDeleted: bool = False
    createdAt: str
    updatedAt: str


class PagedItems(BaseModel):
    page: int
    pageSize: int
    total: int
    items: List[Item]


# --- DB (in-memory) ---
items: List[Item] = []


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_item_id(item_id: str) -> Item:
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


def find_item_name(item_name: str) -> Optional[Item]:
    key = item_name.strip().lower()
    for item in items:
        if not item.isDeleted and item.name.strip().lower() == key:
            return item
    return None

# --- Security ----


def validate_token(token: str) -> bool:
    return token == settings.api_token

# --- Routes ---


@app.get("/")
def home():
    return {"Welcome to menu API"}


@app.get("/api/items", response_model=List[Item])
def list_items(include_deleted: bool = False):
    if include_deleted:
        return items
    return [i for i in items if not i.isDeleted]


@app.get("/api/menu", response_model=PagedItems)
def list_menu(
    search: Optional[str] = Query(None, description="Substring on name"),
    category: Optional[Category] = Query(None),
    available: Optional[bool] = Query(None),
    sort: SortField = Query("name"),
    order: SortOrder = Query("asc"),
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
):
    # 1) base (exclude deleted)
    filtered = [i for i in items if not i.isDeleted]
    # 2) filters
    if category is not None:
        filtered = [i for i in filtered if i.category == category]
    if available is not None:
        filtered = [i for i in filtered if i.isAvailable == available]
    # 3) search substring in name (case-insensitive)
    if search:
        needle = search.strip().lower()
        filtered = [i for i in filtered if needle in i.name.strip().lower()]
    # 4) sorting
    reverse = (order == "desc")
    if sort == "price":
        filtered.sort(key=lambda x: x.price, reverse=reverse)
    else:  # name
        filtered.sort(key=lambda x: x.name.strip().lower(), reverse=reverse)
    # 5) pagination
    total = len(filtered)
    start = (page - 1) * pageSize
    end = start + pageSize
    page_items = filtered[start:end]
    return PagedItems(page=page, pageSize=pageSize, total=total, items=page_items)


@app.post("/api/menu", response_model=Item, status_code=201)
def create_item(payload: ItemCreate, token: str = Depends(get_current_token)):
    constraint = find_item_name(payload.name)
    if payload.price <= 0:
        raise HTTPException(
            status_code=400, detail="Price must be greater than 0")

    if constraint:
        raise HTTPException(status_code=409, detail="Name not unique")
    t = now_iso()
    item = Item(
        id=str(uuid4()),
        name=payload.name,
        category=payload.category,
        price=payload.price,
        isAvailable=payload.isAvailable,
        isDeleted=False,
        createdAt=t,
        updatedAt=t,
    )
    items.append(item)
    return item


@app.patch("/api/menu/{item_id}", response_model=Item)
def update_item(item_id: str, payload: ItemUpdate, token: str = Depends(get_current_token)):

    item = find_item_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Not Found")

    if item.isDeleted:
        raise HTTPException(status_code=400, detail="Item is deleted")

    data = payload.model_dump(exclude_unset=True)

    if "price" in data and data["price"] <= 0:
        raise HTTPException(
            status_code=400, detail="Price must be greater than 0")

    for k, v in data.items():
        setattr(item, k, v)

    item.updatedAt = now_iso()
    return item


@app.delete("/api/menu/{item_id}", response_model=Item)
def delete_item(item_id: str, token: str = Depends(get_current_token)):

    item = find_item_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Not Found")

    # soft delete
    item.isDeleted = True
    item.isAvailable = False
    item.updatedAt = now_iso()
    return item
