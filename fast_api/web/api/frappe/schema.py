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

class CreateItemRequest(BaseModel):
    item_name: str
    item_code: str
    item_group: str
    opening_stock: Optional[float] = 0.0
    valuation_rate: Optional[float] = 0.0
    standard_rate: Optional[float] = 0.0
    end_of_life: Optional[str] = "2099-12-31"
    company_name: str
    warehouse_name: Optional[str] = "Stores - S"

class CreateItemResponse(BaseModel):
    item_code: str


class ListItemsRequest(BaseModel):
    doc_type: str

class ListItemsResponse(BaseModel):
    items: list[dict]


class ReadDocRequest(BaseModel):
    company_id: str

class ReadDocResponse(BaseModel):
    docs: list[dict]

class CreateSupplierRequest(BaseModel):
    supplier_name: str
    gstin: Optional[str] = None
    email_id: Optional[str] = None
    mobile_no: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str

class CreateSupplierResponse(BaseModel):
    supplier_name: str


class CreatePurchaseOrderRequest(BaseModel):
    supplier_name: str
    items: list[dict]
    expected_delivery_date: str
    company_name: str


class CreatePurchaseOrderResponse(BaseModel):
    purchase_order_name: str


class UpdateDocTypeRequest(BaseModel):
    doc_name: Optional[str] = None
    action: Optional[str] = None
    updated_doc: Optional[dict] = None

class UpdateDocTypeResponse(BaseModel):
    message: str

class CreateCustomerRequest(BaseModel):
    customer_name: str
    email_id: str
    mobile_no: str

class CreateCustomerResponse(BaseModel):
    customer_name: str


class CreateSalesOrderRequest(BaseModel):
    customer_name: str
    items: list[dict]
    expected_delivery_date: str
    company_name: str
    transaction_date: str

class CreateSalesOrderResponse(BaseModel):
    sales_order_name: str

class DeleteDocRequest(BaseModel):
    doc_type: str
    doc_name: str
    company_name: str

class DeleteDocResponse(BaseModel):
    message: str

class UpdateDocRequest(BaseModel):
    updated_doc: dict
    company_name: str

class UpdateDocResponse(BaseModel):
    message: str

class GetDocRequest(BaseModel):
    doc_type: str
    doc_name: str
    company_name: str

class GetDocResponse(BaseModel):
    doc: dict
