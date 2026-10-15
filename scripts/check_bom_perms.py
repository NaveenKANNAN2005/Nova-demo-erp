import os
import frappe

os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

perms = frappe.get_all("DocPerm", filters={"parent": "BOM"}, fields=["role", "read", "write", "create"])
for p in perms:
    print(p)