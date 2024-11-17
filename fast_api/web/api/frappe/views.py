from fastapi import APIRouter, HTTPException, status
# from frappeclient import FrappeClient
from fast_api.services.frappe.client import FrappeClient
from fast_api.config import FRAPPE_URL, FRAPPE_USERNAME, FRAPPE_PASSWORD
from fast_api.web.api.frappe.schema import CreateCompanyRequest, CreateCompanyResponse, \
            CreateItemRequest, CreateItemResponse, \
            CreateSupplierRequest, CreateSupplierResponse, \
            CreatePurchaseOrderRequest, CreatePurchaseOrderResponse, \
            ReadDocRequest, ReadDocResponse, \
            UpdateDocTypeRequest, UpdateDocTypeResponse, \
            CreateCustomerRequest, CreateCustomerResponse, \
            CreateSalesOrderRequest, CreateSalesOrderResponse, \
            DeleteDocRequest, DeleteDocResponse, \
            UpdateDocRequest, UpdateDocResponse, \
            GetDocRequest, GetDocResponse

import requests
import random
import string

frappe_conn = FrappeClient(FRAPPE_URL)
frappe_conn.login(FRAPPE_USERNAME, FRAPPE_PASSWORD)

router = APIRouter()

@router.post("/create/company", response_model=CreateCompanyResponse, status_code=status.HTTP_201_CREATED)
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

@router.post("/create/customer", response_model=CreateCustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    request: CreateCustomerRequest
) -> CreateCustomerResponse:
    try:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        create_customer_params = {
            "docstatus": 0,
            "doctype": "Customer",
            "name": f"new-customer-{random_string}",
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "sellprixservices@gmail.com",
            "naming_series": "CUST-.YYYY.-",
            "customer_type": "Company",
            "is_internal_customer": 0,
            "companies": [],
            "language": "en",
            "gst_category": "Unregistered",
            "credit_limits": [],
            "accounts": [],
            "sales_team": [],
            "so_required": 0,
            "dn_required": 0,
            "is_frozen": 0,
            "disabled": 0,
            "portal_users": [],
            "__run_link_triggers": 1,
            "is_primary_address": 0,
            "is_shipping_address": 0,
            "customer_name": request.customer_name,
            "_email_id": request.email_id,
            "_mobile_no": request.mobile_no,
            "country": "India",
            "email_id": request.email_id,
            "mobile_no": request.mobile_no
        }
        customer = frappe_conn.insert(create_customer_params)
        return CreateCustomerResponse(customer_name=customer["name"])
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/create/item", response_model=CreateItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    request: CreateItemRequest
) -> CreateItemResponse:
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
            "standard_rate": request.standard_rate,
            "gst_hsn_code": "010129"
        }
        item = frappe_conn.insert(item_entry_params)
        return CreateItemResponse(item_code=item["name"])
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


@router.post("/create/supplier", response_model=CreateSupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    request: CreateSupplierRequest
) -> CreateSupplierResponse:
    try:
        supplier_create_params = {
            "docstatus": 0,
            "doctype": "Supplier",
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "Administrator",
            "naming_series": "SUP-.YYYY.-",
            "country": "India",
            "supplier_type": "Company",
            "is_transporter": 0,
            "is_internal_supplier": 0,
            "companies": [],
            "language": "en",
            "gst_category": "Registered Regular",
            "accounts": [],
            "allow_purchase_invoice_creation_without_purchase_order": 0,
            "allow_purchase_invoice_creation_without_purchase_receipt": 0,
            "is_frozen": 0,
            "disabled": 0,
            "warn_rfqs": 0,
            "warn_pos": 0,
            "prevent_rfqs": 0,
            "prevent_pos": 0,
            "on_hold": 0,
            "supplier_name": request.supplier_name,
            "gstin": request.gstin,
            "email_id": request.email_id,
            "mobile_no": request.mobile_no,
            "address_line1": request.address_line1,
            "address_line2": request.address_line2,
            "city": request.city,
            "state": request.state,
            "pincode": request.pincode
        }

        supplier = frappe_conn.insert(supplier_create_params)
        return CreateSupplierResponse(supplier_name=supplier["name"])
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


@router.post("/create/purchase-order", response_model=CreatePurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    request: CreatePurchaseOrderRequest
) -> CreatePurchaseOrderResponse:
    try:
        print("Request: ", request)
        #Get the item details from the request
        item_details = request.items
        supplier_name = request.supplier_name
        supplier_details = frappe_conn.get_doc("Supplier", supplier_name)
        print("Supplier Details: ", supplier_details)
        expected_delivery_date = request.expected_delivery_date
        company_name = request.company_name

        #random 6 character string
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        insert_params = {
            "docstatus": 0,
            "doctype": "Purchase Order",
            "name": f"new-purchase-order-{random_string}",
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "sellprixservices@gmail.com",
            "title": supplier_name,
            "naming_series": "PUR-ORD-.YYYY.-",
            "transaction_date": expected_delivery_date,
            "company": company_name,
            "apply_tds": 0,
            "is_reverse_charge": 0,
            "is_subcontracted": 0,
            "currency": "INR",
            "buying_price_list": "Standard Buying",
            "price_list_currency": "INR",
            "ignore_pricing_rule": 0,
            "items": item_details,
            "tax_withholding_net_total": 0,
            "pricing_rules": [],
            "supplied_items": [],
            "taxes": [],
            "disable_rounded_total": 0,
            "apply_discount_on": "Grand Total",
            "payment_schedule": [],
            "status": "Draft",
            "group_same_items": 0,
            "is_internal_supplier": 0,
            "party_account_currency": "INR",
            "is_old_subcontracting_flow": 0,
            "advance_paid": 0,
            "conversion_rate": 1,
            "plc_conversion_rate": 1,
            "base_net_total": 23,
            "net_total": 23,
            "base_total": 23,
            "total": 23,
            "total_qty": 2,
            "rounding_adjustment": 0,
            "grand_total": 23,
            "taxes_and_charges_deducted": 0,
            "taxes_and_charges_added": 0,
            "base_grand_total": 23,
            "base_taxes_and_charges_added": 0,
            "base_taxes_and_charges_deducted": 0,
            "total_taxes_and_charges": 0,
            "base_total_taxes_and_charges": 0,
            "base_rounding_adjustment": 0,
            "rounded_total": 23,
            "base_rounded_total": 23,
            "in_words": "",
            "base_in_words": "",
            "base_discount_amount": 0,
            "total_net_weight": 0,
            "supplier_name": supplier_name,
            "represents_company": "",
            "supplier": supplier_name,
            "supplier_address": f"{supplier_details.get('supplier_primary_address')}",
            "supplier_gstin": f"{supplier_details.get('gstin')}",
            "gst_category": "Registered Regular",
            "address_display": f"{supplier_details.get('supplier_primary_address')}",
            # "tax_category": f"{supplier_details.get('gst_category')}",
            "place_of_supply": f"33-{supplier_details.get('supplier_name')}",
            # "contact_person": f"{supplier_details.get('supplier_name')}",
            "contact_display": f"{supplier_details.get('supplier_name')}",
            "contact_email": f"{supplier_details.get('email_id')}",
            "contact_mobile": f"{supplier_details.get('mobile_no')}",
            "language": "en",
            "payment_terms_template": None,
            "schedule_date": expected_delivery_date
        }
        purchase_order = frappe_conn.insert(insert_params)
        print("Purchase Order: ", purchase_order)
        return CreatePurchaseOrderResponse(purchase_order_name=purchase_order["name"])
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")


@router.post("/update/doctype/{doc_type}", response_model=UpdateDocTypeResponse, status_code=status.HTTP_200_OK)
async def update_doctype(doc_type: str, request: UpdateDocTypeRequest) -> UpdateDocTypeResponse:
    try:
        print("Request: ", request)
        action = request.action
        updated_doc = request.updated_doc
        if action == "submit":
            doc = frappe_conn.get_doc(doc_type, name=updated_doc.get("name"))
            print("Doc: ", doc)
            if doc.get("docstatus") == 0:
                doc["docstatus"] = 1
            print("Doc in update status: ")
            frappe_conn.update(doc)
            return UpdateDocTypeResponse(message="Documents submitted successfully")
        elif action == "cancel":
            doc = frappe_conn.get_doc(doc_type, name=request.doc_name)
            doc["docstatus"] = 2
            frappe_conn.update(doc)
            return UpdateDocTypeResponse(message="Documents cancelled successfully")
        elif action == "Closed" or action == "On Hold":
            print("Doc Type: ", doc_type)
            if doc_type == "Purchase Order":
                response = frappe_conn.update_purchase_status(doc_type, request.doc_name, action)
            elif doc_type == "Sales Order":
                response = frappe_conn.update_sales_status(doc_type, request.doc_name, action)
            print("Response: ", response)
            # print("Updated Doc: ", updated_doc)
            # updated_doc["doctype"] = doc_type
            # frappe_conn.update(updated_doc)
            return UpdateDocTypeResponse(message="Documents updated successfully")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/read/{doc_type}", response_model=ReadDocResponse, status_code=status.HTTP_200_OK)
async def read_doc(doc_type: str, request: ReadDocRequest) -> ReadDocResponse:
    try:
        print(doc_type)
        docs = frappe_conn.get_list(doc_type)
        print(docs)
        print(type(docs))
        return ReadDocResponse(docs=docs)
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/create/sales-order", response_model=CreateSalesOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_sales_order(request: CreateSalesOrderRequest) -> CreateSalesOrderResponse:
    try:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        #get the customer details
        customer_details = frappe_conn.get_doc("Customer", request.customer_name)
        print("Customer Details: ", customer_details)

        insert_params = {
            "docstatus": 0,
            "doctype": "Sales Order",
            "name": f"new-sales-order-{random_string}",
            "__islocal": 1,
            "__unsaved": 1,
            "owner": "sellprixservices@gmail.com",
            "title": request.customer_name,
            "naming_series": "SAL-ORD-.YYYY.-",
            "order_type": "Sales",
            "transaction_date": request.transaction_date,
            "company": request.company_name,
            "skip_delivery_note": 0,
            "is_reverse_charge": 0,
            "is_export_with_gst": 0,
            "currency": "INR",
            "selling_price_list": "Standard Selling",
            "price_list_currency": "INR",
            "ignore_pricing_rule": 0,
            "reserve_stock": 0,
            "items": request.items,
            "taxes": [],
            "disable_rounded_total": 0,
            "apply_discount_on": "Grand Total",
            "packed_items": [],
            "pricing_rules": [],
            "payment_schedule": [],
            "status": "Draft",
            "delivery_status": "Not Delivered",
            "billing_status": "Not Billed",
            "sales_team": [],
            "group_same_items": 0,
            "is_internal_customer": 0,
            "party_account_currency": "INR",
            "advance_paid": 0,
            "conversion_rate": 1,
            "plc_conversion_rate": 1,
            "company_address": None,
            "company_gstin": "",
            "company_address_display": None,
            "total_commission": None,
            "po_no": "",
            "tax_id": None,
            "customer_name": request.customer_name,
            "represents_company": None,
            "customer": request.customer_name,
            "customer_address": None,
            "billing_address_gstin": None,
            "gst_category": "Unregistered",
            "address_display": None,
            "shipping_address_name": None,
            "shipping_address": None,
            "tax_category": "",
            "place_of_supply": f"33-{request.customer_name}",
            "contact_person": f"{request.customer_name}-{request.customer_name}",
            "contact_display": request.customer_name,
            "contact_email": customer_details.get("email_id"),
            "contact_mobile": customer_details.get("mobile_no"),
            "contact_phone": "",
            "customer_group": None,
            "territory": None,
            "language": "en",
            "payment_terms_template": None,
            "delivery_date": request.expected_delivery_date
        }
        sales_order = frappe_conn.insert(insert_params)
        return CreateSalesOrderResponse(sales_order_name=sales_order["name"])
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/delete/", response_model=DeleteDocResponse, status_code=status.HTTP_200_OK)
async def delete_doc(request: DeleteDocRequest) -> DeleteDocResponse:
    try:
        frappe_conn.delete(request.doc_type, request.doc_name)
        return DeleteDocResponse(message="Document deleted successfully")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/update", response_model=UpdateDocResponse, status_code=status.HTTP_200_OK)
async def update_doc(request: UpdateDocRequest) -> UpdateDocResponse:
    try:
        print("Request: ", request)
        frappe_conn.update(request.updated_doc)
        return UpdateDocResponse(message="Document updated successfully")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/get-doc", response_model=GetDocResponse, status_code=status.HTTP_200_OK)
async def get_doc(request: GetDocRequest) -> GetDocResponse:
    try:
        doc = frappe_conn.get_doc(request.doc_type, request.doc_name)
        return GetDocResponse(doc=doc)
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to connect to Frappe server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
