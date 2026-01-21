# Party Ledger Detailed Report (Odoo)

This module provides a **detailed Party Ledger report** in Odoo using a **SQL-based approach**.
It shows **product-level invoice lines**, **credit notes**, **payments**, **opening balance** and a **running balance** with proper debit/credit handling.

---

## 📌 Features

- Partner-wise detailed ledger
- Date range filtering (From / To)
- Correct **Opening Balance** calculation
- Product-wise invoice lines (Qty + Unit Price)
- Credit Notes handled correctly
- Payments & Journal entries included
- Running balance calculation
- Date shown in **single line format**
- Optimized for PDF printing

---

## 📄 Report Columns

| Column | Description |
|------|------------|
| Date | Transaction date (DD-MM-YYYY) |
| Journal | Journal code |
| Document | Invoice / Payment reference |
| Product | Product name (if applicable) |
| Quantity | Product quantity |
| Unit Price | Product unit price |
| Debit | Debit amount |
| Credit | Credit amount |
| Balance | Running balance |

---

## 🧮 Accounting Logic

### 1️⃣ Opening Balance
- Calculated from **all move lines before `date_from`**
- Includes only posted (or draft + posted) moves
- Shown as a single line at top

### 2️⃣ Invoices
- Uses **`aml.balance`** to ensure:
  - Discounts are already applied
  - Correct net amount is shown
- Invoices → **Debit (positive)**
- Credit Notes → **Credit (positive)**

### 3️⃣ Credit Notes
- Product line values shown correctly
- Negative product prices are handled
- No double impact on balance

### 4️⃣ Payments / Journal Entries
- Only Receivable / Payable accounts
- Debit and Credit shown as-is
- Correctly affects running balance

### 5️⃣ Running Balance
Calculated using:
```sql
SUM(debit - credit) OVER (ORDER BY date, document, product)
