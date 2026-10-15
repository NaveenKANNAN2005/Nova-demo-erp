# ERPNext Project 01: Developer Handover & Acceptance Evidence

**Project:** Nova Industries — ERPNext Implementation  
**Site:** `nova.local`  
**ERPNext Version:** 17.x.x-develop  
**Company:** Nova Industries (`NI`)  
**Base Currency:** INR (₹)  
**Timezone:** Asia/Kolkata  
**Fiscal Year:** 2026-2027 (01-04-2026 to 31-03-2027)  

---

## 1. Executive Summary

All functional, statutory, workflow, security, and non-functional requirements specified in `ERPNext_Project_01_Customer_Requirements.pdf` have been **100% satisfied** and validated on `nova.local`.

- **Configuration-First Architecture:** Built strictly using standard Frappe / ERPNext controllers, hooks, and configuration defaults. No ERPNext core files were modified.
- **Perpetual Inventory & Valuation:** Perpetual inventory is active with the standard Indian Chart of Accounts and **FIFO** stock valuation.
- **GST Taxation Engine:** Intra-state (9% CGST + 9% SGST) and Inter-state (18% IGST) sample templates and ledger accounts configured and verified.
- **State-Linked Address Master:** Official Address records with State and PIN codes created and dynamically linked to Nova Industries (Tamil Nadu), Customers (`ABC Retailers` in Tamil Nadu, `Metro Office Supplies` in Karnataka), and Suppliers (`Chennai Components` in Tamil Nadu, `Bengaluru Devices` in Karnataka).
- **Full Procurement & Sales Lifecycles:** Demonstrated end-to-end flows, including optional upstream documents (**Material Request** `MAT-MR-2026-00001` and **Quotation** `SAL-QTN-2026-00001`).
- **Comprehensive RBAC Verification:** All 5 user personas (`purchase_user`, `sales_user`, `stock_user`, `accounts_user`, and `manager_readonly`) tested for both permitted duties and restricted actions.
- **Flawless Accounting & Stock Reconciliation:** General Ledger balanced to ₹0.00 discrepancy (₹101,690.00 Debits == ₹101,690.00 Credits). Inventory valuation matches the Stock In Hand balance (₹49,850.00) to the cent.

---

## 2. Configuration Inventory

### 2.1 Company Defaults & Accounts

| Parameter | Configuration Value |
| :--- | :--- |
| **Company Name** | Nova Industries |
| **Abbreviation** | `NI` |
| **Country / Currency** | India / `INR` |
| **Fiscal Year** | `2026-2027` (01-04-2026 to 31-03-2027) |
| **Default Primary Warehouse** | `Main Warehouse - NI` |
| **Default Cost Center** | `Main - NI` |
| **Default Bank Account** | `HDFC Bank - NI` |
| **Default Cash Account** | `Cash - NI` |
| **Receivable Control Account** | `Debtors - NI` (Parent: `Accounts Receivable - NI`) |
| **Payable Control Account** | `Creditors - NI` (Parent: `Accounts Payable - NI`) |
| **Default Income Account** | `Sales - NI` |
| **Default Expense Account** | `Cost of Goods Sold - NI` |
| **Stock In Hand Account** | `Stock In Hand - NI` |
| **Stock Interim Accounts** | `Stock Received But Not Billed - NI`, `Stock Delivered But Not Billed - NI` |
| **Stock Adjustment Account** | `Stock Adjustment - NI` |
| **Temporary Opening Account** | `Temporary Opening - NI` |
| **Stock Valuation Method** | `FIFO` |
| **Default Buying Price List** | `Standard Buying` |
| **Default Selling Price List** | `Standard Selling` |

### 2.2 Tax Accounts & Templates

* **Tax Asset Accounts (Input GST under `Tax Assets - NI`):**
  * `Input CGST - NI` (Rate: 9%)
  * `Input SGST - NI` (Rate: 9%)
  * `Input IGST - NI` (Rate: 18%)
* **Tax Liability Accounts (Output GST under `Duties and Taxes - NI`):**
  * `Output CGST - NI` (Rate: 9%)
  * `Output SGST - NI` (Rate: 9%)
  * `Output IGST - NI` (Rate: 18%)
* **Purchase Tax Templates:**
  * `Intra-State GST 18% - NI`: Line 1: `Input CGST - NI` (9%), Line 2: `Input SGST - NI` (9%)
  * `Inter-State GST 18% - NI`: Line 1: `Input IGST - NI` (18%)
* **Sales Tax Templates:**
  * `Intra-State GST 18% - NI`: Line 1: `Output CGST - NI` (9%), Line 2: `Output SGST - NI` (9%)
  * `Inter-State GST 18% - NI`: Line 1: `Output IGST - NI` (18%)

---

## 3. Master Data Inventory

### 3.1 Items & Pricing (Item Group: `Electronics Accessories`)

| Item Code | Item Name | UOM | Valuation Rate | Selling Rate | Opening Qty | Opening Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `USB-C-001` | USB-C Cable 1m | Nos | ₹120.00 | ₹200.00 | 100 Nos | ₹12,000.00 |
| `MOUSE-001` | Wireless Mouse | Nos | ₹350.00 | ₹550.00 | 50 Nos | ₹17,500.00 |
| `KEYBOARD-001`| USB Keyboard | Nos | ₹500.00 | ₹750.00 | 30 Nos | ₹15,000.00 |
| **TOTAL** | | | | | **180 Nos** | **₹44,500.00** |

*Opening Stock Voucher:* `MAT-RECO-2026-00001` posted on `2026-04-01`.

### 3.2 Parties & Addresses

| Entity Type | Name | Address Title | City, State | Pincode | Tax Context | Credit / Payment Terms |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Company** | `Nova Industries` | Nova Industries HQ | Chennai, Tamil Nadu | 600002 | Operating State | Base Entity |
| **Customer** | `ABC Retailers` | ABC Retailers Chennai | Chennai, Tamil Nadu | 600001 | Intra-State | Credit Limit: ₹100,000.00 |
| **Customer** | `Metro Office Supplies`| Metro Office Supplies Bengaluru | Bengaluru, Karnataka | 560001 | Inter-State | Credit Limit: ₹150,000.00 |
| **Supplier** | `Chennai Components` | Chennai Components Guindy | Chennai, Tamil Nadu | 600032 | Intra-State | 30 Days Net (`30 Days Net - NI`) |
| **Supplier** | `Bengaluru Devices` | Bengaluru Devices Electronic City| Bengaluru, Karnataka | 560100 | Inter-State | 15 Days Net (`15 Days Net - NI`) |

---

## 4. Role-Based Access Control (RBAC) Verification Matrix

Tested dynamically with `frappe.set_user()` and standard permission hooks:

| User Account | Functional Persona | Allowed Actions Verified | Restricted Actions Verified (Blocked) |
| :--- | :--- | :--- | :--- |
| `purchase_user@nova.local` | Purchase User | Can create & submit `Purchase Order` (**YES**) | Cannot create `User` or alter system setup (**BLOCKED**) |
| `sales_user@nova.local` | Sales User | Can create & submit `Sales Order` (**YES**) | Cannot delete or modify `Company` records (**BLOCKED**) |
| `stock_user@nova.local` | Stock User | Can create & submit `Delivery Note` (**YES**) | Cannot modify `System Settings` (**BLOCKED**) |
| `accounts_user@nova.local` | Accounts User | Can create & submit `Payment Entry` (**YES**) | Cannot create `User` accounts (**BLOCKED**) |
| `manager_readonly@nova.local` | Read-only Manager | Can read `Sales Order`, `GL Entry`, Reports (**YES**) | Cannot create, submit, or edit transactions (**BLOCKED**) |

---

## 5. End-to-End Test Evidence Matrix

| Test ID | Flow / Feature | Executed Voucher Sequence | Verified Outcomes & Financials | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P-01** | Standard Purchase | `PUR-ORD-2026-00003`<br>$\rightarrow$ `MAT-PRE-2026-00001`<br>$\rightarrow$ `ACC-PINV-2026-00001`<br>$\rightarrow$ `ACC-PAY-2026-00001` | Stock +40 Nos (`USB-C-001`). AP ₹5,664.00 created (with 9% CGST + 9% SGST) and cleared in full via HDFC Bank. | **PASS** |
| **P-02** | Partial Receipt | `PUR-ORD-2026-00004` (20 Nos)<br>$\rightarrow$ `MAT-PRE-2026-00002` (12 Nos)<br>$\rightarrow$ `ACC-PINV-2026-00002` (₹4,956)<br>$\rightarrow$ `MAT-PRE-2026-00003` (8 Nos) | Received 12 first (8 pending). Invoiced only 12 with 18% IGST. Received remaining 8 later. Cumulative receipt 20/20. | **PASS** |
| **P-03** | Supplier Controls & Partial Payment | `ACC-PAY-2026-00002` (₹2,000)<br>$\rightarrow$ `ACC-PAY-2026-00003` (₹2,956)<br>`PUR-ORD-2026-00005` (Cancelled) | Invoice status transitioned to `Partly Paid` with ₹2,956 outstanding, then to `Paid`. Cancelled PO verified docstatus=2. | **PASS** |
| **S-01** | Standard Sale | `SAL-ORD-2026-00003`<br>$\rightarrow$ `MAT-DN-2026-00001`<br>$\rightarrow$ `ACC-SINV-2026-00001`<br>$\rightarrow$ `ACC-PAY-2026-00005` | Stock -10 Nos (`USB-C-001`). AR ₹2,360.00 created (with 9% CGST + 9% SGST) and cleared in full via HDFC Bank. | **PASS** |
| **S-02** | Partial Delivery & Excess Stock Control | `SAL-ORD-2026-00004` (15 Nos)<br>$\rightarrow$ `MAT-DN-2026-00002` (10 Nos)<br>$\rightarrow$ `MAT-DN-2026-00003` (5 Nos) | Delivered 10 first (5 pending). Excess delivery attempted and controlled. Delivered remaining 5. Cumulative delivered 15/15. | **PASS** |
| **S-03** | Partial Customer Receipt | `ACC-SINV-2026-00002` (₹6,490)<br>$\rightarrow$ `ACC-PAY-2026-00006` (50%: ₹3,245)<br>$\rightarrow$ `ACC-PAY-2026-00007` (50%: ₹3,245) | Invoice status transitioned to `Partly Paid` with ₹3,245 outstanding, then to `Paid`. AR matches remaining balance. | **PASS** |
| **OPT-01** | Material Request | `MAT-MR-2026-00001` | Material Request for 20 Nos `KEYBOARD-001` created and submitted for warehouse replenishment. | **PASS** |
| **OPT-02** | Customer Quotation | `SAL-QTN-2026-00001` | Customer quotation for `ABC Retailers` created and submitted with pre-tax price ₹750 and 18% intra-state GST. | **PASS** |
| **SEC-01** | Least-Privilege Role Testing | Dynamic session switch | Read-only manager blocked from creating invoices (`PermissionError`), while list and report views succeeded. | **PASS** |
| **ACC-01** | Full Ledger Reconciliation | GL, Trial Balance, Stock Balance | Total Debits: **₹101,690.00** == Total Credits: **₹101,690.00**. Discrepancy = **₹0.00**. Stock In Hand = **₹49,850.00**. | **PASS** |

---

## 6. Financial & Inventory Reconciliation

### 6.1 Tax Ledgers Balance Summary

| Tax Account Name | Account Type | Root Type | Total Debit (Input) | Total Credit (Output) | Net Tax Position |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Input CGST - NI` | Tax | Asset | ₹432.00 | ₹0.00 | ₹432.00 (Input Credit) |
| `Input SGST - NI` | Tax | Asset | ₹432.00 | ₹0.00 | ₹432.00 (Input Credit) |
| `Input IGST - NI` | Tax | Asset | ₹756.00 | ₹0.00 | ₹756.00 (Input Credit) |
| `Output CGST - NI` | Tax | Liability | ₹0.00 | ₹180.00 | ₹180.00 (Output Due) |
| `Output SGST - NI` | Tax | Liability | ₹0.00 | ₹180.00 | ₹180.00 (Output Due) |
| `Output IGST - NI` | Tax | Liability | ₹0.00 | ₹990.00 | ₹990.00 (Output Due) |

### 6.2 Stock Balance Reconciliation (`Main Warehouse - NI`)

| Item Code | Item Description | Opening Qty | Qty Received | Qty Delivered | Closing Qty | Valuation Rate | Closing Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `USB-C-001` | USB-C Cable 1m | 100 Nos | +40 Nos (P-01) | -10 Nos (S-01) | **130 Nos** | ₹120.00 | ₹15,600.00 |
| `MOUSE-001` | Wireless Mouse | 50 Nos | +20 Nos (P-02) | -15 Nos (S-02) | **55 Nos** | ₹350.00 | ₹19,250.00 |
| `KEYBOARD-001`| USB Keyboard | 30 Nos | 0 | 0 | **30 Nos** | ₹500.00 | ₹15,000.00 |
| **TOTAL** | | **180 Nos** | **+60 Nos** | **-25 Nos** | **215 Nos** | | **₹49,850.00** |

* **General Ledger Balance (`Stock In Hand - NI`):** **₹49,850.00** (Exact 1:1 match).

---

## 7. Customer Sign-Off Checklist

- [x] **Procure-to-Pay:** Can create, track, and pay purchases from PO through Purchase Receipt, Purchase Invoice, and Payment Entry.
- [x] **Order-to-Cash:** Can create, track, deliver, invoice, and collect customer payments from Sales Order through Delivery Note, Sales Invoice, and Payment Entry.
- [x] **Stock Tracking:** Quantities change strictly on physical movements (Purchase Receipt / Delivery Note) and reconcile with the Stock Ledger.
- [x] **Receivables & Payables:** Invoices and payments update party balances accurately, supporting partial payments and clearing upon completion.
- [x] **Tax Visibility:** GST amounts (CGST, SGST, IGST) post to their dedicated ledger accounts and reconcile with transaction bases.
- [x] **Standard Reporting:** Standard reports (General Ledger, Trial Balance, Stock Balance, Accounts Receivable, Accounts Payable) match transaction history.
- [x] **Access Control:** User roles restrict unauthorized document modifications while maintaining read-only visibility for reporting personas.
- [x] **Clean Handover:** All configuration and repeatable test evidence have been documented and tested on `nova.local`.
