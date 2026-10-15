import os
import frappe
from frappe.utils.password import update_password
os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

print("--- Setting up Users and Roles ---")

role_name = "Read-only Manager"
if not frappe.db.exists("Role", role_name):
    r = frappe.new_doc("Role")
    r.role_name = role_name
    r.desk_access = 1
    r.insert()
    print(f"Created role: {role_name}")

target_doctypes = [
    "Sales Order", "Purchase Order", "Delivery Note", "Purchase Receipt",
    "Sales Invoice", "Purchase Invoice", "Payment Entry", "Item", "Customer", 
    "Supplier", "GL Entry", "Stock Ledger Entry"
]
for dt in target_doctypes:
    if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": role_name}):
        try:
            perm = frappe.new_doc("Custom DocPerm")
            perm.parent = dt
            perm.parenttype = "DocType"
            perm.parentfield = "permissions"
            perm.role = role_name
            perm.read = 1
            perm.report = 1
            perm.write = 0
            perm.create = 0
            perm.submit = 0
            perm.cancel = 0
            perm.delete = 0
            perm.insert()
        except Exception as e:
            pass

users_config = [
    {"email": "purchase_user@nova.local", "first_name": "Purchase", "last_name": "User", "roles": ["Purchase User", "Stock User"]},
    {"email": "sales_user@nova.local", "first_name": "Sales", "last_name": "User", "roles": ["Sales User", "Stock User"]},
    {"email": "stock_user@nova.local", "first_name": "Stock", "last_name": "User", "roles": ["Stock User"]},
    {"email": "accounts_user@nova.local", "first_name": "Accounts", "last_name": "User", "roles": ["Accounts User"]},
    {"email": "manager_readonly@nova.local", "first_name": "Read-only", "last_name": "Manager", "roles": [role_name]},
]

strong_pass = "NovaInd#2026!SecureBench"

for u in users_config:
    email = u["email"]
    if not frappe.db.exists("User", email):
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = u["first_name"]
        user.last_name = u["last_name"]
        user.enabled = 1
        user.send_welcome_email = 0
        for r in u["roles"]:
            user.append("roles", {"role": r})
        user.flags.ignore_password_policy = True
        user.insert(ignore_permissions=True)
        update_password(email, strong_pass)
        print(f"Created user: {email} with roles {u['roles']}")
    else:
        user = frappe.get_doc("User", email)
        user.enabled = 1
        current_roles = [r.role for r in user.roles]
        for r in u["roles"]:
            if r not in current_roles:
                user.append("roles", {"role": r})
        user.save(ignore_permissions=True)
        update_password(email, strong_pass)
        print(f"Updated user: {email}")

frappe.db.commit()
print("Users setup completed successfully!")