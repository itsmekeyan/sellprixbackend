from fastapi import APIRouter, HTTPException, status
# from frappeclient import FrappeClient
from fast_api.services.frappe.client import FrappeClient
from fast_api.config import FRAPPE_URL, FRAPPE_USERNAME, FRAPPE_PASSWORD
from fast_api.web.api.frappe.schema import CreateCompanyRequest, CreateCompanyResponse, \
            InsertItemRequest, InsertItemResponse, ListItemsRequest, ListItemsResponse

import requests

frappe_conn = FrappeClient(FRAPPE_URL)
frappe_conn.login(FRAPPE_USERNAME, FRAPPE_PASSWORD)

router = APIRouter()

@router.post("/create-company", response_model=CreateCompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CreateCompanyRequest
) -> CreateCompanyResponse:
    try:
        #check if workspace type is provided
        if request.workspace_type is None:
            request.workspace_type = "Transit"
        company_create_params = {
            "docstatus": 0,
            "doctype": "Company",
            "name": request.company_name,
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "Administrator",
            "country": "India",
            "is_group": 0,
            "create_chart_of_accounts_based_on": "",
            "allow_account_creation_against_child_company": 0,
            "book_advance_payments_in_separate_party_account": 0,
            "reconcile_on_advance_payment_date": 0,
            "auto_exchange_rate_revaluation": 0,
            "auto_err_frequency": "Daily",
            "submit_err_jv": 0,
            "enable_perpetual_inventory": 1,
            "enable_provisional_accounting_for_non_stock_items": 0,
            "company_name": request.company_name,
            "abbr": request.abbreviation,
            "default_currency": "INR",
            "date_of_establishment": request.date_of_establishment,
            "domain": request.domain,
            "tax_id": request.tax_id,
            "parent_company": "",
            "existing_company": ""
        }
        company = frappe_conn.insert(company_create_params)

        # Create warehouse
        warehouse_create_params = {
            "docstatus": 0,
            "doctype": "Warehouse",
            "name": request.warehouse_name,
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "Administrator",
            "disabled": 0,
            "is_group": 0,
            "is_rejected_warehouse": 0,
            "company": request.company_name,
            "warehouse_name": request.warehouse_name,
            "phone_no": request.phone_no,
            "address_line_1": request.address1,
            "address_line_2": request.address2,
            "city": request.city,
            "state": request.state,
            "pin": request.pin,
            "warehouse_type": request.workspace_type
        }
        warehouse = frappe_conn.insert(warehouse_create_params)

        return CreateCompanyResponse(
            company_name=company["name"],
            warehouse_name=warehouse["name"]
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Frappe server"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/insert-item", response_model=InsertItemResponse, status_code=status.HTTP_201_CREATED)
async def insert_item(
    request: InsertItemRequest
) -> InsertItemResponse:
    try:
        item_entry_params = {
            "docstatus": 0,
            "doctype": "Item",
            "name": request.item_name,
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "Administrator@gmail.com",
            "naming_series": "STO-ITEM-.YYYY.-",
            "stock_uom": "Nos",
            "disabled": 0,
            "allow_alternative_item": 0,
            "is_stock_item": 1,
            "has_variants": 0,
            "is_fixed_asset": 0,
            "auto_create_assets": 0,
            "is_grouped_asset": 0,
            "uoms": [],
            "end_of_life": request.end_of_life,
            "default_material_request_type": "Purchase",
            "valuation_method": "",
            "allow_negative_stock": 0,
            "barcodes": [],
            "reorder_levels": [],
            "has_batch_no": 0,
            "create_new_batch": 0,
            "has_expiry_date": 0,
            "retain_sample": 0,
            "has_serial_no": 0,
            "variant_based_on": "Item Attribute",
            "attributes": [],
            "enable_deferred_expense": 0,
            "enable_deferred_revenue": 0,
            "item_defaults": [
                {
                    "docstatus": 0,
                    "doctype": "Item Default",
                    "name": request.item_name,
                    "__islocal": 1,
                    "__unsaved": 1,
                    "owner": "Administrator@gmail.com",
                    "company": request.company_name,
                    "default_warehouse": request.warehouse_name,
                    "parent": request.item_name,
                    "parentfield": "item_defaults",
                    "parenttype": "Item",
                    "idx": 1,
                    "__unedited": True
                }
            ],
            "min_order_qty": 0,
            "is_purchase_item": 1,
            "is_customer_provided_item": 0,
            "delivered_by_supplier": 0,
            "supplier_items": [],
            "country_of_origin": "India",
            "grant_commission": 1,
            "is_sales_item": 1,
            "customer_items": [],
            "taxes": [],
            "inspection_required_before_purchase": 0,
            "inspection_required_before_delivery": 0,
            "include_item_in_manufacturing": 1,
            "is_sub_contracted_item": 0,
            "item_code": request.item_code,
            "item_name": request.item_name,
            "item_group": request.item_group,
            "opening_stock": request.opening_stock,
            "valuation_rate": request.valuation_rate,
            "standard_rate": request.standard_rate
        }
        item = frappe_conn.insert(item_entry_params)
        return InsertItemResponse(item_code=item["name"])
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Frappe server"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/list-items", response_model=ListItemsResponse, status_code=status.HTTP_200_OK)
async def list_items(
    request: ListItemsRequest
) -> ListItemsResponse:
    try:
        items = frappe_conn.get_list(request.doc_type)
        return ListItemsResponse(items=items)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Frappe server"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
