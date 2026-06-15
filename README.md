🏪 Grocery Store Management System

A complete **web-based e-commerce management system** for grocery stores, built with **Python Flask**, **MySQL**, and **Bootstrap**.

---

## ✨ **Key Features**

### 🔐 **Authentication**
- Admin login & signup system
- Secure password hashing
- Session management

### 📦 **Product Management**
- Create, read, update, delete products
- Search by product name or ID
- Organize by units of measurement (UOM)
- Price management

### 🛒 **Order Management**
- Create new orders
- View all orders
- Edit existing orders
- Search orders by customer, date, or order ID
- Auto-calculate order totals
- Order history tracking

### 📊 **Inventory Management**
- Real-time stock tracking
- Low stock alerts
- Reorder level management
- Manual stock adjustments
- Complete audit trail of all stock movements
- Stock transaction history

### 📈 **Analytics & Reports**
- Revenue trends (daily, monthly)
- Top selling products analysis
- Revenue distribution by product
- Customer spending analytics
- Inventory status overview
- Date range filtering
- Interactive charts (Line, Bar, Pie charts)

### 🔄 **Smart Features**
- Auto-reduce inventory when orders created
- Update inventory when orders edited
- Track all inventory changes with reasons
- Professional dashboard UI
- Responsive design (mobile & desktop)

---

## 🛠️ **Tech Stack**

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3, Flask |
| **Database** | MySQL 8.0 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript, jQuery |
| **Charts** | Chart.js |
| **Authentication** | Werkzeug (password hashing) |
| **Server** | Gunicorn (production) |

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- MySQL 8.0+
- Git

### **Installation**

1. **Clone Repository**
```bash
git clone https://github.com/Kanimunasinghe/Grocery-Store-Management.git
cd Grocery-Store-Management
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Database**
```bash
mysql -u root -p
CREATE DATABASE gs;
```

5. **Run Application**
```bash
python server.py
```

6. **Access System**
```
Frontend: http://127.0.0.1:5500/UI/
Backend API: http://127.0.0.1:5000
```

---

## 📊 **Database Schema**

Main tables:
- **admin_users** - Admin authentication
- **products** - Product catalog
- **orders** - Customer orders
- **order_details** - Order line items
- **inventory** - Stock levels
- **stock_transactions** - Audit trail
- **uom** - Units of measurement

---

## 🎯 **Core Functionality**

### **1. Dashboard**
- Overview statistics
- Quick access to all modules
- Real-time data

### **2. Product Management**
- Add new products
- Search & filter
- Edit product details
- Delete products
- Manage pricing

### **3. Order Management**
- Create orders with multiple products
- Edit existing orders
- Auto-adjust inventory
- Search & filter orders
- View order history

### **4. Inventory Management**
- Track stock levels
- Set reorder thresholds
- Manual adjustments with notes
- View stock transaction history
- Low stock alerts
- Shortage calculations

### **5. Analytics**
- Revenue trend analysis
- Product performance metrics
- Customer insights
- Inventory valuation
- Period-based filtering
- Export ready data

---
