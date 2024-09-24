def get_user_data_schema():
    return {
        "type": "object",
        "properties": {
            "ordered_by": {
                "type": "string",
                "description": "Name of the person who placed the order, also called the buyer."
            },
            "buyer_email": {
                "type": "string",
                "description": "Email of the person who placed the order."
            },
            "buyer_name": {
                "type": "string",
                "description": "Name of the buyer."
            },
            "requestor_name": {
                "type": "string",
                "description": "Name of the requestor."
            },
            "requestor_email": {
                "type": "string",
                "description": "Email of the requestor."
            }
        },
        "required": [
            "ordered_by", "buyer_email", "buyer_name", "requestor_name", "requestor_email"
        ],
        "additionalProperties": False
    }


def get_product_data_schema():
    return {
        "type": "object",
        "properties": {
            "po_number": {
                "type": "string",
                "description": "Order number of the Invoice."
            },
            "order_date": {
                "type": "string",
                "format": "date",
                "description": "Date when the order was placed in dd-mm-yyyy format."
            },
            "delivery_date": {
                "type": "string",
                "format": "date",
                "description": "Date when the order will be delivered in dd-mm-yyyy format."
            },
            "po_total_aed": {
                "type": "string",
                "description": "Total amount of the purchase order in AED."
            },
            "tax_total_aed": {
                "type": "string",
                "description": "Total tax amount of the purchase order in AED."
            },
            "grand_total_aed": {
                "type": "string",
                "description": "Grand total amount of the purchase order including tax in AED."
            }
        },
        "required": [
            "po_number", "order_date", "delivery_date", "po_total_aed", "tax_total_aed", "grand_total_aed"
        ],
        "additionalProperties": False
    }


def get_supplier_data_schema():
    return {
        "type": "object",
        "properties": {
            "bill_to": {
                "type": "string",
                "description": "Address where the bill is sent."
            },
            "supplier_address": {
                "type": "string",
                "description": "Address of the supplier."
            }
        },
        "required": ["bill_to"],
        "additionalProperties": False
    }


def get_product_item_schema():
    return {
        "type": "object",
        "properties": {
            "product_group": {
                "type": "string",
                "description": "Group or category of the product."
            },
            "product_code": {
                "type": "string",
                "description": "Code of the product. It sometimes be in the format like A|129056, read the pipe sign carefully."
            },
            "uom": {
                "type": "string",
                "description": "Unit of measure of the product."
            },
            "product_name": {
                "type": "string",
                "description": "Name of the product."
            },
            "unit_price_aed": {
                "type": "string",
                "description": "Price per unit of the product in AED."
            },
            "tax_rate": {
                "type": "string",
                "description": "Tax rate percentage of the product."
            },
            "amount_aed": {
                "type": "string",
                "description": "Total amount of the product in AED."
            },
            "quantity": {
                "type": "string",
                "description": "Quantity ordered also referred as Qty."
            },
            "line_total_aed": {
                "type": "string",
                "description": "Line total amount of the product in AED."
            }
        },
        "required": [
            "product_group", "product_code", "uom", "product_name",
            "unit_price_aed", "tax_rate", "amount_aed", "quantity", "line_total_aed"
        ],
        "additionalProperties": False
    }
