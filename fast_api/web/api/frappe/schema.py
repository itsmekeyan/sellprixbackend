from pydantic import BaseModel
from typing import Optional


class CreateCompanyRequest(BaseModel):
    """Request schema for creating a company and warehouse."""
    company_name: str
    warehouse_name: str
    abbreviation: str
    date_of_establishment: str
    domain: str
    tax_id: str
    address1: str
    address2: str
    city: str
    state: str
    pin: str
    phone_no: str

    workspace_type: Optional[str] = None

class CreateCompanyResponse(BaseModel):
    """Response schema for creating a company and warehouse."""
    company_name: str
    warehouse_name: str

class InsertItemRequest(BaseModel):
    item_name: str
    item_code: str
    item_group: str
    opening_stock: float
    valuation_rate: float
    standard_rate: float
    end_of_life: str
    company_name: str
    warehouse_name: str

class InsertItemResponse(BaseModel):
    item_code: str


class ListItemsRequest(BaseModel):
    doc_type: str

class ListItemsResponse(BaseModel):
    items: list[dict]
