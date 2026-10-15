import frappe
import os
os.chdir('/home/naveen/frappe-bench/sites')
frappe.init('nova.local')
frappe.connect()

from frappe.www.nova_portal import get_context
ctx = {}
get_context(ctx)
print("SUCCESS! Keys:", list(ctx.keys()))
