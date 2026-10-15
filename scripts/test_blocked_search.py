import os
import frappe

os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

from frappe.desk.search import search_link

# Set user to sales_user@nova.local who has module_profile = "Nova Trading Operations" (blocking Manufacturing)
frappe.set_user("sales_user@nova.local")
print("Current user:", frappe.session.user)

# Test 1: Awesomebar search for BOM
from frappe.utils.global_search import search
from frappe.desk.search import search_widget

print("\n--- Test 1: Checking doctype access via frappe.has_permission ---")
print("Has permission on BOM?:", frappe.has_permission("BOM", ptype="read"))
print("Has permission on Work Order?:", frappe.has_permission("Work Order", ptype="read"))

print("\n--- Test 2: Checking Awesomebar search results ---")
import frappe.desk.search as search_mod
try:
    results = search_mod.search_link("DocType", "BOM")
    print("search_link('DocType', 'BOM') returned:", results)
except Exception as e:
    print("Search error:", e)

frappe.set_user("Administrator")