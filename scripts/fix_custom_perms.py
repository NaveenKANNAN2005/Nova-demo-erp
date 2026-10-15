import os
import frappe
from frappe.permissions import reset_perms, add_permission

os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

target_doctypes = [
    "Sales Order", "Purchase Order", "Delivery Note", "Purchase Receipt",
    "Sales Invoice", "Purchase Invoice", "Payment Entry", "Item", "Customer", 
    "Supplier", "GL Entry", "Stock Ledger Entry", "Material Request", "Quotation"
]

role_name = "Read-only Manager"

for dt in target_doctypes:
    # Reset custom perms back to standard
    reset_perms(dt)
    # Now use Frappe standard add_permission API which properly sets up custom perms
    add_permission(dt, role_name, 0)
    # Set read=1, report=1 and ensure write=0, create=0, submit=0, cancel=0
    cdp = frappe.get_doc("Custom DocPerm", {"parent": dt, "role": role_name})
    cdp.read = 1
    cdp.report = 1
    cdp.write = 0
    cdp.create = 0
    cdp.submit = 0
    cdp.cancel = 0
    cdp.delete = 0
    cdp.save()
    print(f"Properly configured custom perms for {dt} with {role_name}")

frappe.db.commit()
frappe.clear_cache()
print("All doctypes perms reset & properly configured!")