import os
import frappe

os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

print("--- 1. Creating Module Profile: Nova Trading Operations ---")
mp_name = "Nova Trading Operations"
blocked = [
    "Manufacturing", "Quality Management", "Support", "Projects", 
    "Assets", "Subcontracting", "Maintenance", "CRM", "Website", 
    "Telephony", "Portal", "EDI", "Bulk Transaction"
]

if not frappe.db.exists("Module Profile", mp_name):
    mp = frappe.new_doc("Module Profile")
    mp.module_profile_name = mp_name
    for mod in blocked:
        mp.append("block_modules", {"module": mod})
    mp.insert()
    print(f"Created Module Profile: {mp_name} blocking {len(blocked)} modules.")
else:
    mp = frappe.get_doc("Module Profile", mp_name)
    mp.set("block_modules", [])
    for mod in blocked:
        mp.append("block_modules", {"module": mod})
    mp.save()
    print(f"Updated Module Profile: {mp_name}")

print("\n--- 2. Assigning Module Profile to Users ---")
users = [
    "purchase_user@nova.local", "sales_user@nova.local", 
    "stock_user@nova.local", "accounts_user@nova.local", 
    "manager_readonly@nova.local"
]
for email in users:
    if frappe.db.exists("User", email):
        u = frappe.get_doc("User", email)
        u.module_profile = mp_name
        u.save(ignore_permissions=True)
        print(f"Assigned {mp_name} to {email}")

print("\n--- 3. Hiding Out-of-Scope Workspaces ---")
workspaces_to_hide = [
    "Manufacturing", "Quality", "Support", "Projects", 
    "Assets", "CRM", "Website", "Build", "Integrations", "Automation"
]
for ws_name in workspaces_to_hide:
    if frappe.db.exists("Workspace", ws_name):
        ws = frappe.get_doc("Workspace", ws_name)
        ws.is_hidden = 1
        ws.save(ignore_permissions=True)
        print(f"Hidden Workspace: {ws_name}")

print("\n--- 4. Active Visible Workspaces ---")
visible_ws = frappe.get_all("Workspace", filters={"is_hidden": 0, "public": 1}, fields=["name", "title", "module"])
for v in visible_ws:
    print(f"  • Visible: {v.name:20} (Module: {v.module})")

frappe.db.commit()
frappe.clear_cache()
print("\nModule restrictions applied and Desk updated successfully!")