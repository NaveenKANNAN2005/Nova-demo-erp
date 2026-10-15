# Nova Industries - Production ERPNext 17

Official deployment repository for **Nova Industries (`NI`)**, a trading and distribution company based in Chennai, Tamil Nadu, India.

---

## 🚀 1-Click Deployment on Render.com

This repository is pre-configured with **Render Blueprints (`render.yaml`)** and a production **`Dockerfile`**.

### Steps to Deploy:
1. Log into your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Connect this repository: `NaveenKANNAN2005/Nova-demo-erp`.
4. Click **Apply**.
5. Render will automatically:
   - Build the Docker container.
   - Attach a 10 GB persistent storage disk for database and attachments.
   - Start Redis and MariaDB services.
   - Restore the verified **Nova Industries** production database snapshot.
   - Bind to Render's dynamic `$PORT` and issue a free SSL certificate.

Your live instance will be available at:
👉 **`https://nova-industries-erp.onrender.com`**

---

## 🔑 Login Credentials

| Role | Username / Email | Password | Allowed Modules |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `Administrator` | `NovaInd#2026!SecureBench` | All (System Settings) |
| **Purchase Specialist** | `purchase_user@nova.local` | `NovaInd#2026!SecureBench` | Buying, Stock |
| **Sales Operations** | `sales_user@nova.local` | `NovaInd#2026!SecureBench` | Selling, Stock |
| **Stock & Warehouse** | `stock_user@nova.local` | `NovaInd#2026!SecureBench` | Stock, Items |
| **Senior Accountant** | `accounts_user@nova.local` | `NovaInd#2026!SecureBench` | Accounting, Payments |
| **Executive / General Manager** | `manager_readonly@nova.local` | `NovaInd#2026!SecureBench` | Read-Only (All) |

---

## 📦 What's Pre-Configured in this Release

1. **Company & Localization**:
   - Company: **Nova Industries** (`NI`)
   - Country: India, Currency: INR (₹), FY: 2026–2027
   - GSTIN: `33AAAAA0000A1Z5` (Tamil Nadu - 33)
   - Perpetual Inventory: Enabled (FIFO valuation method).
2. **Item Masters & Initial Stock**:
   - `USB-C-001` (Fast Charging Cable)
   - `MOUSE-001` (Wireless Optical Mouse)
   - `KEYBOARD-001` (Mechanical Gaming Keyboard)
   - Total Stock Valuation: **₹49,850.00**
3. **Verified Accounts & Ledgers**:
   - Bank: `HDFC Bank - NI` (₹35,744.00)
   - Cash: `Cash - NI` (₹10,000.00)
   - General Ledger Equilibrium: Debits **₹101,690.00** = Credits **₹101,690.00** (Zero Variance).
4. **Clean Workspaces**:
   - Unused modules (`Manufacturing`, `Quality`, `Support`, `Assets`, `CRM`, etc.) are hidden via `Module Profile`.
   - Users only see the 4 modules they need: **Accounting**, **Buying**, **Selling**, and **Stock**.

---

## 📁 Repository Structure

```
├── Dockerfile                  # Container runtime for Render
├── render.yaml                 # Render Blueprint specification
├── render-entrypoint.sh        # Service startup & snapshot restore logic
├── sites/
│   └── nova.local/
│       ├── site_config.json    # Hardened production site config (developer_mode=0)
│       └── private/backups/    # Verified production database snapshot (1.1 MB)
├── scripts/                    # Automation, testing, and acceptance scripts
└── docs/                       # Complete customer handover and runbook docs
```
