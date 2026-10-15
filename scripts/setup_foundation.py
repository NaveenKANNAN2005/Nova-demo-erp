import os
import frappe
os.chdir("/home/naveen/frappe-bench/sites")
frappe.init("nova.local")
frappe.connect()

print("--- 1. Warehouse Setup ---")
wh_name = "Main Warehouse - NI"
if not frappe.db.exists("Warehouse", wh_name):
    wh = frappe.new_doc("Warehouse")
    wh.warehouse_name = "Main Warehouse"
    wh.company = "Nova Industries"
    wh.parent_warehouse = "All Warehouses - NI"
    wh.insert()
    print(f"Created warehouse: {wh.name}")
else:
    print(f"Warehouse already exists: {wh_name}")

# Set default warehouse in company and stock settings
company = frappe.get_doc("Company", "Nova Industries")
company.default_warehouse = wh_name
company.save()
print(f"Company default warehouse set to {company.default_warehouse}")

stock_settings = frappe.get_doc("Stock Settings")
stock_settings.default_warehouse = wh_name
stock_settings.valuation_method = "FIFO"
stock_settings.save()
print("Stock settings updated: FIFO and Main Warehouse")

print("\n--- 2. Tax Accounts ---")
tax_accounts = [
    # Input Taxes (Asset under Tax Assets - NI)
    {"account_name": "Input CGST", "parent_account": "Tax Assets - NI", "root_type": "Asset", "account_type": "Tax", "tax_rate": 9},
    {"account_name": "Input SGST", "parent_account": "Tax Assets - NI", "root_type": "Asset", "account_type": "Tax", "tax_rate": 9},
    {"account_name": "Input IGST", "parent_account": "Tax Assets - NI", "root_type": "Asset", "account_type": "Tax", "tax_rate": 18},
    # Output Taxes (Liability under Duties and Taxes - NI)
    {"account_name": "Output CGST", "parent_account": "Duties and Taxes - NI", "root_type": "Liability", "account_type": "Tax", "tax_rate": 9},
    {"account_name": "Output SGST", "parent_account": "Duties and Taxes - NI", "root_type": "Liability", "account_type": "Tax", "tax_rate": 9},
    {"account_name": "Output IGST", "parent_account": "Duties and Taxes - NI", "root_type": "Liability", "account_type": "Tax", "tax_rate": 18},
]

created_accounts = {}
for ta in tax_accounts:
    full_name = f"{ta['account_name']} - NI"
    if not frappe.db.exists("Account", full_name):
        acc = frappe.new_doc("Account")
        acc.account_name = ta["account_name"]
        acc.company = "Nova Industries"
        acc.parent_account = ta["parent_account"]
        acc.root_type = ta["root_type"]
        acc.account_type = ta["account_type"]
        acc.tax_rate = ta["tax_rate"]
        acc.insert()
        print(f"Created Account: {acc.name}")
        created_accounts[ta["account_name"]] = acc.name
    else:
        print(f"Account exists: {full_name}")
        created_accounts[ta["account_name"]] = full_name

print("\n--- 3. Tax Templates ---")
# Purchase Tax Templates
# Intra-State Purchase
intra_p_title = "Intra-State GST 18% - NI"
if not frappe.db.exists("Purchase Taxes and Charges Template", intra_p_title):
    pt = frappe.new_doc("Purchase Taxes and Charges Template")
    pt.title = intra_p_title
    pt.company = "Nova Industries"
    pt.is_default = 1
    pt.append("taxes", {
        "category": "Total",
        "charge_type": "On Net Total",
        "account_head": "Input CGST - NI",
        "description": "CGST @ 9%",
        "rate": 9
    })
    pt.append("taxes", {
        "category": "Total",
        "charge_type": "On Net Total",
        "account_head": "Input SGST - NI",
        "description": "SGST @ 9%",
        "rate": 9
    })
    pt.insert()
    print(f"Created Purchase Tax Template: {pt.name}")

# Inter-State Purchase
inter_p_title = "Inter-State GST 18% - NI"
if not frappe.db.exists("Purchase Taxes and Charges Template", inter_p_title):
    pt = frappe.new_doc("Purchase Taxes and Charges Template")
    pt.title = inter_p_title
    pt.company = "Nova Industries"
    pt.append("taxes", {
        "category": "Total",
        "charge_type": "On Net Total",
        "account_head": "Input IGST - NI",
        "description": "IGST @ 18%",
        "rate": 18
    })
    pt.insert()
    print(f"Created Purchase Tax Template: {pt.name}")

# Sales Tax Templates
# Intra-State Sales
intra_s_title = "Intra-State GST 18% - NI"
if not frappe.db.exists("Sales Taxes and Charges Template", intra_s_title):
    st = frappe.new_doc("Sales Taxes and Charges Template")
    st.title = intra_s_title
    st.company = "Nova Industries"
    st.is_default = 1
    st.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": "Output CGST - NI",
        "description": "Output CGST @ 9%",
        "rate": 9
    })
    st.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": "Output SGST - NI",
        "description": "Output SGST @ 9%",
        "rate": 9
    })
    st.insert()
    print(f"Created Sales Tax Template: {st.name}")

# Inter-State Sales
inter_s_title = "Inter-State GST 18% - NI"
if not frappe.db.exists("Sales Taxes and Charges Template", inter_s_title):
    st = frappe.new_doc("Sales Taxes and Charges Template")
    st.title = inter_s_title
    st.company = "Nova Industries"
    st.append("taxes", {
        "charge_type": "On Net Total",
        "account_head": "Output IGST - NI",
        "description": "Output IGST @ 18%",
        "rate": 18
    })
    st.insert()
    print(f"Created Sales Tax Template: {st.name}")

print("\n--- 4. Payment Terms ---")
for days in [15, 30]:
    t_name = f"{days} Days"
    if not frappe.db.exists("Payment Term", t_name):
        pt = frappe.new_doc("Payment Term")
        pt.payment_term_name = t_name
        pt.credit_days = days
        pt.insert()
        print(f"Created Payment Term: {pt.name}")

    tmpl_name = f"{days} Days Net - NI"
    if not frappe.db.exists("Payment Terms Template", tmpl_name):
        ptt = frappe.new_doc("Payment Terms Template")
        ptt.template_name = tmpl_name
        ptt.append("terms", {
            "payment_term": t_name,
            "invoice_portion": 100,
            "credit_days": days
        })
        ptt.insert()
        print(f"Created Payment Terms Template: {ptt.name}")

print("\n--- 5. Item Group & Items ---")
ig_name = "Electronics Accessories"
if not frappe.db.exists("Item Group", ig_name):
    ig = frappe.new_doc("Item Group")
    ig.item_group_name = ig_name
    ig.parent_item_group = "All Item Groups"
    ig.is_group = 0
    ig.insert()
    print(f"Created Item Group: {ig.name}")

items_data = [
    {"item_code": "USB-C-001", "item_name": "USB-C Cable 1m", "valuation_rate": 120.0, "selling_rate": 200.0, "opening_qty": 100},
    {"item_code": "MOUSE-001", "item_name": "Wireless Mouse", "valuation_rate": 350.0, "selling_rate": 550.0, "opening_qty": 50},
    {"item_code": "KEYBOARD-001", "item_name": "USB Keyboard", "valuation_rate": 500.0, "selling_rate": 750.0, "opening_qty": 30},
]

for item_info in items_data:
    code = item_info["item_code"]
    if not frappe.db.exists("Item", code):
        it = frappe.new_doc("Item")
        it.item_code = code
        it.item_name = item_info["item_name"]
        it.item_group = ig_name
        it.stock_uom = "Nos"
        it.is_stock_item = 1
        it.default_warehouse = wh_name
        it.valuation_rate = item_info["valuation_rate"]
        it.standard_rate = item_info["selling_rate"]
        it.insert()
        print(f"Created Item: {it.name}")
    else:
        print(f"Item exists: {code}")

    # Item Prices
    # Buying
    if not frappe.db.exists("Item Price", {"item_code": code, "price_list": "Standard Buying"}):
        ip = frappe.new_doc("Item Price")
        ip.item_code = code
        ip.price_list = "Standard Buying"
        ip.price_list_rate = item_info["valuation_rate"]
        ip.currency = "INR"
        ip.insert()
        print(f"Created Standard Buying price for {code}: {item_info['valuation_rate']}")
    # Selling
    if not frappe.db.exists("Item Price", {"item_code": code, "price_list": "Standard Selling"}):
        ip = frappe.new_doc("Item Price")
        ip.item_code = code
        ip.price_list = "Standard Selling"
        ip.price_list_rate = item_info["selling_rate"]
        ip.currency = "INR"
        ip.insert()
        print(f"Created Standard Selling price for {code}: {item_info['selling_rate']}")

print("\n--- 6. Opening Stock via Stock Reconciliation ---")
if not frappe.db.exists("Stock Reconciliation", {"company": "Nova Industries", "purpose": "Opening Stock", "docstatus": 1}):
    sr = frappe.new_doc("Stock Reconciliation")
    sr.company = "Nova Industries"
    sr.purpose = "Opening Stock"
    sr.posting_date = "2026-04-01"
    sr.posting_time = "00:00:01"
    sr.expense_account = "Temporary Opening - NI"
    for item_info in items_data:
        sr.append("items", {
            "item_code": item_info["item_code"],
            "warehouse": wh_name,
            "qty": item_info["opening_qty"],
            "valuation_rate": item_info["valuation_rate"]
        })
    sr.insert()
    sr.submit()
    print(f"Submitted Opening Stock Reconciliation: {sr.name}")
else:
    print("Opening Stock Reconciliation already submitted.")

print("\n--- 7. Customers ---")
customers_data = [
    {
        "name": "ABC Retailers", 
        "state": "Tamil Nadu", 
        "credit_limit": 100000, 
        "tax_treatment": "Intra-state"
    },
    {
        "name": "Metro Office Supplies", 
        "state": "Karnataka", 
        "credit_limit": 150000, 
        "tax_treatment": "Inter-state"
    }
]

for cd in customers_data:
    c_name = cd["name"]
    if not frappe.db.exists("Customer", c_name):
        c = frappe.new_doc("Customer")
        c.customer_name = c_name
        c.customer_group = "Commercial"
        c.territory = "India"
        c.customer_type = "Company"
        c.append("credit_limits", {
            "company": "Nova Industries",
            "credit_limit": cd["credit_limit"]
        })
        c.insert()
        print(f"Created Customer: {c.name}")
    else:
        print(f"Customer exists: {c_name}")

print("\n--- 8. Suppliers ---")
suppliers_data = [
    {
        "name": "Chennai Components", 
        "state": "Tamil Nadu", 
        "payment_terms": "30 Days Net - NI"
    },
    {
        "name": "Bengaluru Devices", 
        "state": "Karnataka", 
        "payment_terms": "15 Days Net - NI"
    }
]

for sd in suppliers_data:
    s_name = sd["name"]
    if not frappe.db.exists("Supplier", s_name):
        s = frappe.new_doc("Supplier")
        s.supplier_name = s_name
        s.supplier_group = "Distributor"
        s.supplier_type = "Company"
        s.payment_terms = sd["payment_terms"]
        s.insert()
        print(f"Created Supplier: {s.name}")
    else:
        print(f"Supplier exists: {s_name}")

frappe.db.commit()
print("\n--- Milestone 2 setup finished cleanly! ---")