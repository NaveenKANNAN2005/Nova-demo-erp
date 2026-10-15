import frappe
from frappe import _
import json

def get_context(context):
    context.no_cache = 1
    data = get_portal_data()
    context.portal_data_json = json.dumps(data)
    context.title = 'Nova Industries - Enterprise Role Portal'
    return context

@frappe.whitelist(allow_guest=True)
def get_portal_data():
    company = 'Nova Industries'
    currency = '₹'
    
    bank_accounts = [
        {'name': 'HDFC Bank - NI', 'type': 'Bank', 'code': 'HDFC-001'},
        {'name': 'Cash - NI', 'type': 'Cash', 'code': 'CASH-001'},
        {'name': 'Stock In Hand - NI', 'type': 'Stock Asset', 'code': 'STOCK-001'},
        {'name': 'Debtors - NI', 'type': 'Receivable', 'code': 'DEBT-001'},
        {'name': 'Creditors - NI', 'type': 'Payable', 'code': 'CRED-001'}
    ]
    
    for acc in bank_accounts:
        bal = frappe.db.sql(
            'SELECT COALESCE(SUM(debit) - SUM(credit), 0) FROM 	abGL Entry WHERE company = %s AND account = %s',
            (company, acc['name'])
        )[0][0]
        acc['balance'] = float(bal)
        acc['formatted_balance'] = f'₹{float(bal):,.2f}'

    gl_totals = frappe.db.sql(
        'SELECT COALESCE(SUM(debit), 0), COALESCE(SUM(credit), 0) FROM 	abGL Entry WHERE company = %s',
        (company,)
    )[0]
    total_debit = float(gl_totals[0])
    total_credit = float(gl_totals[1])
    diff = round(total_debit - total_credit, 2)
    is_balanced = (diff == 0.0)

    items_raw = frappe.get_all(
        'Item',
        filters={'disabled': 0},
        fields=['name', 'item_name', 'item_group', 'stock_uom', 'standard_rate']
    )
    items = []
    total_stock_value = 0.0
    for it in items_raw:
        bin_data = frappe.db.sql(
            'SELECT COALESCE(SUM(actual_qty), 0), COALESCE(SUM(stock_value), 0), COALESCE(AVG(valuation_rate), 0) '
            'FROM 	abBin WHERE item_code = %s',
            (it.name,)
        )[0]
        qty = float(bin_data[0])
        val = float(bin_data[1])
        rate = float(bin_data[2]) if bin_data[2] else float(it.standard_rate or 0)
        
        if val == 0.0 and qty > 0:
            val = qty * rate
            
        total_stock_value += val
        items.append({
            'item_code': it.name,
            'item_name': it.item_name,
            'stock_uom': it.stock_uom,
            'standard_rate': float(it.standard_rate or 0),
            'actual_qty': qty,
            'valuation_rate': rate,
            'stock_value': val,
            'formatted_value': f'₹{val:,.2f}',
            'status': 'In Stock' if qty > 10 else ('Low Stock' if qty > 0 else 'Out of Stock')
        })

    pos = frappe.get_all(
        'Purchase Order',
        filters={'company': company},
        fields=['name', 'transaction_date', 'supplier', 'grand_total', 'status', 'per_received', 'per_billed'],
        order_by='creation desc',
        limit=20
    )
    for po in pos:
        po['formatted_total'] = f'₹{float(po.grand_total):,.2f}'

    sos = frappe.get_all(
        'Sales Order',
        filters={'company': company},
        fields=['name', 'transaction_date', 'customer', 'grand_total', 'status', 'per_delivered', 'per_billed'],
        order_by='creation desc',
        limit=20
    )
    for so in sos:
        so['formatted_total'] = f'₹{float(so.grand_total):,.2f}'

    pinvs = frappe.get_all(
        'Purchase Invoice',
        filters={'company': company},
        fields=['name', 'posting_date', 'supplier', 'grand_total', 'outstanding_amount', 'status'],
        order_by='creation desc',
        limit=20
    )
    for pinv in pinvs:
        pinv['formatted_total'] = f'₹{float(pinv.grand_total):,.2f}'
        pinv['formatted_outstanding'] = f'₹{float(pinv.outstanding_amount):,.2f}'

    sinvs = frappe.get_all(
        'Sales Invoice',
        filters={'company': company},
        fields=['name', 'posting_date', 'customer', 'grand_total', 'outstanding_amount', 'status'],
        order_by='creation desc',
        limit=20
    )
    for sinv in sinvs:
        sinv['formatted_total'] = f'₹{float(sinv.grand_total):,.2f}'
        sinv['formatted_outstanding'] = f'₹{float(sinv.outstanding_amount):,.2f}'

    payments = frappe.get_all(
        'Payment Entry',
        filters={'company': company},
        fields=['name', 'posting_date', 'party', 'payment_type', 'paid_amount', 'mode_of_payment'],
        order_by='creation desc',
        limit=20
    )
    for pay in payments:
        pay['formatted_amount'] = f'₹{float(pay.paid_amount):,.2f}'

    quotations = frappe.get_all(
        'Quotation',
        filters={'company': company},
        fields=['name', 'transaction_date', 'party_name', 'grand_total', 'status'],
        order_by='creation desc',
        limit=10
    )
    for q in quotations:
        q['formatted_total'] = f'₹{float(q.grand_total):,.2f}'

    material_requests = frappe.get_all(
        'Material Request',
        filters={'company': company},
        fields=['name', 'transaction_date', 'material_request_type', 'status', 'per_ordered'],
        order_by='creation desc',
        limit=10
    )

    suppliers = frappe.get_all('Supplier', fields=['name', 'supplier_group', 'supplier_type', 'country'])
    customers = frappe.get_all('Customer', fields=['name', 'customer_group', 'customer_type', 'territory'])

    roles_config = [
        {
            'id': 'manager',
            'name': 'General Manager / Executive',
            'user_email': 'manager_readonly@nova.local',
            'role_badge': 'Executive Read-Only',
            'badge_color': '#8b5cf6',
            'avatar': '👑',
            'description': 'Full business 360° visibility, Executive KPIs, P&L, Balanced GL audit & Liquid Reserves.',
            'allowed_sections': ['kpis', 'financials', 'audit', 'inventory_summary', 'parties']
        },
        {
            'id': 'purchase',
            'name': 'Purchase Specialist',
            'user_email': 'purchase_user@nova.local',
            'role_badge': 'Buying Operations',
            'badge_color': '#3b82f6',
            'avatar': '🛒',
            'description': 'Procurement workflow, Material Requests, Purchase Orders, Goods Receipt Notes (GRN) & Vendor Ledger.',
            'allowed_sections': ['purchase_kpis', 'purchase_orders', 'material_requests', 'suppliers', 'pinvoices']
        },
        {
            'id': 'sales',
            'name': 'Sales Operations Lead',
            'user_email': 'sales_user@nova.local',
            'role_badge': 'Selling Operations',
            'badge_color': '#10b981',
            'avatar': '💼',
            'description': 'Customer Quotations, Sales Orders, Order Fulfillment (Delivery Notes) & Customer Accounts.',
            'allowed_sections': ['sales_kpis', 'sales_orders', 'quotations', 'customers', 'sinvoices']
        },
        {
            'id': 'stock',
            'name': 'Warehouse & Stock Master',
            'user_email': 'stock_user@nova.local',
            'role_badge': 'Inventory Operations',
            'badge_color': '#f59e0b',
            'avatar': '📦',
            'description': 'Real-time Item Stock Levels, Warehouse Valuation, Goods Inward/Outward movements.',
            'allowed_sections': ['stock_kpis', 'inventory_table', 'warehouses', 'item_master']
        },
        {
            'id': 'accounts',
            'name': 'Senior Accountant',
            'user_email': 'accounts_user@nova.local',
            'role_badge': 'Finance & Taxation',
            'badge_color': '#06b6d4',
            'avatar': '💰',
            'description': 'Sales & Purchase Invoices, Payment Reconciliations, GST CGST/SGST/IGST Taxation & General Ledger.',
            'allowed_sections': ['accounts_kpis', 'sinvoices', 'pinvoices', 'payments', 'gst_summary', 'gl_entries']
        }
    ]

    total_revenue = sum([float(s.grand_total) for s in sinvs if s.status != 'Cancelled'])
    total_procurement = sum([float(p.grand_total) for p in pinvs if p.status != 'Cancelled'])
    liquid_reserves = next((a['balance'] for a in bank_accounts if a['name'] == 'HDFC Bank - NI'), 0) +                       next((a['balance'] for a in bank_accounts if a['name'] == 'Cash - NI'), 0)

    return {
        'company': company,
        'gstin': '33AAAAA0000A1Z5',
        'state': 'Tamil Nadu (33)',
        'currency': currency,
        'executive_kpis': {
            'total_revenue': f'₹{total_revenue:,.2f}',
            'total_procurement': f'₹{total_procurement:,.2f}',
            'stock_asset_value': f'₹{total_stock_value:,.2f}',
            'liquid_reserves': f'₹{liquid_reserves:,.2f}',
            'gl_total_debit': f'₹{total_debit:,.2f}',
            'gl_total_credit': f'₹{total_credit:,.2f}',
            'gl_diff': f'₹{diff:,.2f}',
            'is_balanced': is_balanced
        },
        'bank_accounts': bank_accounts,
        'items': items,
        'purchase_orders': pos,
        'sales_orders': sos,
        'purchase_invoices': pinvs,
        'sales_invoices': sinvs,
        'payments': payments,
        'quotations': quotations,
        'material_requests': material_requests,
        'suppliers': suppliers,
        'customers': customers,
        'roles': roles_config
    }
