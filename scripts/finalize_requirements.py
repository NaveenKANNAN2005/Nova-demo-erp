import os
import frappe
from frappe.utils import nowdate, add_days

os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

print("--- 1. Creating Addresses with State and Links ---")

addresses_to_create = [
    {
        "title": "Nova Industries HQ",
        "line1": "12 Mount Road",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600002",
        "link_doctype": "Company",
        "link_name": "Nova Industries",
        "is_primary_address": 1
    },
    {
        "title": "ABC Retailers Chennai",
        "line1": "45 Anna Salai",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600001",
        "link_doctype": "Customer",
        "link_name": "ABC Retailers",
        "is_primary_address": 1
    },
    {
        "title": "Metro Office Supplies Bengaluru",
        "line1": "78 MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560001",
        "link_doctype": "Customer",
        "link_name": "Metro Office Supplies",
        "is_primary_address": 1
    },
    {
        "title": "Chennai Components Guindy",
        "line1": "101 Guindy Industrial Estate",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600032",
        "link_doctype": "Supplier",
        "link_name": "Chennai Components",
        "is_primary_address": 1
    },
    {
        "title": "Bengaluru Devices Electronic City",
        "line1": "22 Electronic City Phase 1",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560100",
        "link_doctype": "Supplier",
        "link_name": "Bengaluru Devices",
        "is_primary_address": 1
    }
]

for addr in addresses_to_create:
    title = addr["title"]
    if not frappe.db.exists("Address", {"address_title": title}):
        doc = frappe.new_doc("Address")
        doc.address_title = title
        doc.address_type = "Office"
        doc.address_line1 = addr["line1"]
        doc.city = addr["city"]
        doc.state = addr["state"]
        doc.country = "India"
        doc.pincode = addr["pincode"]
        doc.append("links", {
            "link_doctype": addr["link_doctype"],
            "link_name": addr["link_name"]
        })
        doc.insert()
        print(f"Created Address: {title} for {addr['link_doctype']} {addr['link_name']}")
    else:
        print(f"Address already exists: {title}")

print("\n--- 2. Material Request (Optional P2P Step) ---")
if not frappe.db.exists("Material Request", {"company": "Nova Industries"}):
    mr = frappe.new_doc("Material Request")
    mr.company = "Nova Industries"
    mr.material_request_type = "Purchase"
    mr.transaction_date = nowdate()
    mr.schedule_date = add_days(nowdate(), 7)
    mr.append("items", {
        "item_code": "KEYBOARD-001",
        "qty": 20,
        "warehouse": "Main Warehouse - NI",
        "schedule_date": add_days(nowdate(), 7)
    })
    mr.insert()
    mr.submit()
    print(f"Created & Submitted Material Request: {mr.name} for 20 Nos KEYBOARD-001")
else:
    print("Material Request already exists.")

print("\n--- 3. Quotation (Optional O2C Step) ---")
if not frappe.db.exists("Quotation", {"company": "Nova Industries"}):
    quot = frappe.new_doc("Quotation")
    quot.quotation_to = "Customer"
    quot.party_name = "ABC Retailers"
    quot.company = "Nova Industries"
    quot.transaction_date = nowdate()
    quot.valid_till = add_days(nowdate(), 30)
    quot.selling_price_list = "Standard Selling"
    quot.append("items", {
        "item_code": "KEYBOARD-001",
        "qty": 5,
        "rate": 750.0
    })
    quot.taxes_and_charges = "Intra-State GST 18% - NI"
    quot.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": "Output CGST - NI",
        "description": "Output CGST @ 9%",
        "rate": 9
    })
    quot.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": "Output SGST - NI",
        "description": "Output SGST @ 9%",
        "rate": 9
    })
    quot.insert()
    quot.submit()
    print(f"Created & Submitted Quotation: {quot.name} (Valid till {quot.valid_till})")
else:
    print("Quotation already exists.")

print("\n--- 4. Multi-Role Permission Verification Tests ---")

role_tests = [
    {
        "user": "purchase_user@nova.local",
        "role_name": "Purchase User",
        "can_action": ("Purchase Order", "create"),
        "cannot_action": ("User", "create")
    },
    {
        "user": "sales_user@nova.local",
        "role_name": "Sales User",
        "can_action": ("Sales Order", "create"),
        "cannot_action": ("Company", "delete")
    },
    {
        "user": "stock_user@nova.local",
        "role_name": "Stock User",
        "can_action": ("Delivery Note", "create"),
        "cannot_action": ("System Settings", "write")
    },
    {
        "user": "accounts_user@nova.local",
        "role_name": "Accounts User",
        "can_action": ("Payment Entry", "create"),
        "cannot_action": ("User", "create")
    },
    {
        "user": "manager_readonly@nova.local",
        "role_name": "Read-only Manager",
        "can_action": ("Sales Order", "read"),
        "cannot_action": ("Sales Order", "create")
    }
]

for rt in role_tests:
    u = rt["user"]
    frappe.set_user(u)
    
    # Check allowed action
    dt_can, action_can = rt["can_action"]
    has_perm = frappe.has_permission(dt_can, ptype=action_can, user=u)
    print(f"User {u} ({rt['role_name']}): Can {action_can} {dt_can}? {'YES' if has_perm else 'NO'}")
    assert has_perm, f"Expected {u} to have {action_can} on {dt_can}"
    
    # Check restricted action
    dt_cannot, action_cannot = rt["cannot_action"]
    has_restricted_perm = frappe.has_permission(dt_cannot, ptype=action_cannot, user=u)
    print(f"User {u} ({rt['role_name']}): Can {action_cannot} {dt_cannot}? {'YES (VIOLATION)' if has_restricted_perm else 'NO (BLOCKED AS EXPECTED)'}")
    assert not has_restricted_perm, f"Security violation: {u} should NOT have {action_cannot} on {dt_cannot}"

frappe.set_user("Administrator")
frappe.db.commit()
print("\nAll remaining elements & role tests completed and verified successfully!")