"""
Menu Management API - FastAPI Backend
Main application file with all routes, models, and business logic.
Uses in-memory storage for simplicity in MVP.
"""

from fastapi import Depends, FastAPI, Header, Query, HTTPException
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
from datetime import datetime, timezone
from app.settings import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI(
    title="FastAPI App",
    version="0.1.0",
)

# HTTP Bearer authentication for protected endpoints
security = HTTPBearer()


# CORS configuration to allow requests from frontend development server
# In production, this should be restricted to specific domains
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Only allow these origins
    allow_credentials=True,  # Allow cookies if needed
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
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

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float):
        if v < 0:
            raise ValueError("Price must be ≥ 0")

        decimal_value = Decimal(str(v))
        if decimal_value.as_tuple().exponent < -2:

            decimal_value = decimal_value.quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
        return float(decimal_value)


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

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Price must be ≥ 0")

            decimal_value = Decimal(str(v))
            if decimal_value.as_tuple().exponent < -2:

                decimal_value = decimal_value.quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP)
            return float(decimal_value)
        return v


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
# Simple list acting as in-memory database
items: List[Item] = []


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Dependency function to extract and validate Bearer token

    This function is injected into protected endpoints using FastAPI's
    dependency injection system. It validates the token against the
    configured API token from settings.
    """

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
    """Find non-deleted item by name (case-insensitive)

    Used to enforce unique name constraint. Compares normalized
    (lowercase, trimmed) names to ensure case-insensitive uniqueness.
    """
    key = item_name.strip().lower()
    for item in items:
        if not item.isDeleted and item.name.strip().lower() == key:
            return item
    return None

# --- Security ----


def validate_token(token: str) -> bool:
    return token == settings.api_tokenA

# --- Routes ---


@app.get("/")
def home():
    return {"Welcome to menu API"}


@app.get("/api/items", response_model=List[Item])
def list_items(include_deleted: bool = False):
    """Get all items (including deleted if specified)

    Simple endpoint for debugging/admin purposes.
    Not used by the main frontend application.
    """
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
    """Main endpoint: Get paginated, filtered, sorted menu items

    Implements complex filtering logic:
    - Exclude soft-deleted items
    - Apply category filter if specified
    - Apply availability filter if specified
    - Apply text search (case-insensitive substring)
    - Sort by specified field and order
    - Apply pagination (offset-based)

    """

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


@app.get("/api/menu/{item_id}", response_model=Item)
def get_item(item_id: str, include_deleted: bool = Query(False, description="Include soft-deleted items")):
    """Get single item by ID

    By default, returns 404 if item is soft-deleted.
    Set include_deleted=true to retrieve soft-deleted items.
    """

    item = find_item_id(item_id)

    # If not including deleted and item is deleted, return 404
    if not include_deleted and item.isDeleted:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@app.post("/api/menu", response_model=Item, status_code=201)
def create_item(payload: ItemCreate, token: str = Depends(get_current_token)):
    """Create new menu item (protected endpoint)

    Business rules enforced:
    - Name must be unique among non-deleted items (case-insensitive)
    - Price validation already handled by Pydantic model
    - Auto-generate UUID, timestamps
    """

    # Check for name uniqueness constraint
    constraint = find_item_name(payload.name)

    if constraint:
        raise HTTPException(status_code=409, detail="Name not unique")
    # Generate current timestamp
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

    # Add to in-memory database
    items.append(item)
    # Return created item with 201 status code
    return item


@app.patch("/api/menu/{item_id}", response_model=Item)
def update_item(item_id: str, payload: ItemUpdate, token: str = Depends(get_current_token)):
    """Update existing item (partial update, protected endpoint)

    Uses PATCH semantics: only provided fields are updated.
    model_dump(exclude_unset=True) ensures only provided fields are included.
    """

    item = find_item_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Not Found")

    if item.isDeleted:
        raise HTTPException(status_code=400, detail="Item is deleted")

    data = payload.model_dump(exclude_unset=True)

    for k, v in data.items():
        setattr(item, k, v)

    item.updatedAt = now_iso()
    return item


@app.delete("/api/menu/{item_id}", response_model=Item)
def delete_item(item_id: str, token: str = Depends(get_current_token)):
    """Soft delete menu item (protected endpoint)

    Instead of removing from database, we:
    - Set isDeleted = True
    - Set isAvailable = False (consistency)
    - Update timestamp
    Item will be excluded from all listings.
    """

    item = find_item_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Not Found")

    # Soft delete implementation
    item.isDeleted = True
    item.isAvailable = False
    item.updatedAt = now_iso()
    return item
