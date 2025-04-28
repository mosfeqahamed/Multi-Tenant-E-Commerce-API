# Multi-Tenant E-Commerce API

A Django REST Framework (DRF) backend providing a JWT-secured, role-based, multi-tenant e-commerce API.  
Vendors can manage their own products (with images), customers can place orders, and admins have full access.

---

## Features

- **JWT Authentication** via `djangorestframework-simplejwt`  
- **Role-Based Access Control** (`admin` / `vendor` / `customer`)  
- **Multi-Tenant**: vendors only see & manage their own products & orders  
- **Product Image Uploads** (served under `/media/products/`)  
- **Pagination**, **Filtering**, **Search**, **Ordering** out of the box  
- **Django Admin** UI for superusers  
- **Signals**: email notifications to vendors when new orders are placed  
- **Optional Redis Cache** configuration for hot endpoints  

---

## Tech Stack

- Python 3.10+  
- Django 4.x  
- Django REST Framework  
- djangorestframework-simplejwt  
- django-filters  
- Pillow (for `ImageField`)  
- Redis (optional, for caching)  

---

## Getting Started

### 1. Clone & Virtual Environment

bash command

git clone https://github.com/mosfeqahamed/Multi-Tenant-E-Commerce-API
cd ecommerce_project

# create & activate a virtualenv
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt




### Authentication & User Management

| Endpoint                       | Method | Description                                                                                                                                          | Access     |
|--------------------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| **POST** `/api/auth/register/` | POST   | Register a new user.  
Body JSON:
```json
{
  "username": "jane",
  "email":    "jane@example.com",
  "password": "secret",
  "role":     "vendor",            # admin | vendor | customer
  "company_name": "Jane’s Shop"    # only if role == vendor
}
```                                                                                       | Public     |
| **POST** `/api/token/`         | POST   | Obtain JWT access & refresh tokens.  
Body JSON:
```json
{ "username": "jane", "password": "secret" }
```                                                                                       | Public     |
| **POST** `/api/token/refresh/` | POST   | Refresh your access token.  
Body JSON:
```json
{ "refresh": "<refresh_token>" }
```                                                                                       | Public     |

---

### Vendor Management (Read-Only)

| Endpoint                    | Method | Description                                                   | Access               |
|-----------------------------|--------|---------------------------------------------------------------|----------------------|
| **GET** `/api/vendors/`     | GET    | List all vendor profiles (paginated)                          | Authenticated users  |
| **GET** `/api/vendors/{id}/`| GET    | Retrieve details for vendor with ID `{id}`                    | Authenticated users  |

---

### Product Management (CRUD + Search/Filter)

| Endpoint                          | Method  | Description                                                                                                                                                                           | Access                            |
|-----------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| **GET** `/api/products/`          | GET     | List products (paginated). Supports query params:  
- `?search=` (name/description)  
- `?ordering=price,-created_at`  
- `?vendor=<id>&min_price=&max_price=`                                                                                                                   | All authenticated users           |
| **GET** `/api/products/{id}/`     | GET     | Retrieve product `{id}` (includes image URL)                                                                                                                                        | All authenticated users           |
| **POST** `/api/products/`         | POST    | Create a new product.  
Form-data: `name`, `price`, `description`, `image` (file). Vendor is inferred from your JWT’d account.                                                                                 | Vendors (own) & Admins            |
| **PUT** `/api/products/{id}/`     | PUT     | Replace all fields of product `{id}` (re-upload image if needed).                                                                                                                   | Vendor owner or Admin             |
| **PATCH** `/api/products/{id}/`   | PATCH   | Partially update product `{id}` (e.g. change price only).                                                                                                                           | Vendor owner or Admin             |
| **DELETE** `/api/products/{id}/`  | DELETE  | Delete product `{id}` (and its image file).                                                                                                                                         | Vendor owner or Admin             |

---

### Order Management (CRUD + Multi-Role Views)

| Endpoint                          | Method  | Description                                                                                                                                                          | Access                                             |
|-----------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| **GET** `/api/orders/`            | GET     | List orders (paginated).  
- **Admin** sees all  
- **Vendor** sees orders containing their products  
- **Customer** sees only their own                                                                                                                        | Authenticated, scoped by role                      |
| **GET** `/api/orders/{id}/`       | GET     | Retrieve order `{id}`, including line-items (`product` + `quantity`).                                                                                                 | Same scoping as list orders                        |
| **POST** `/api/orders/`           | POST    | Place a new order.  
Body JSON:
```json
{
  "items": [
    { "product": 3, "quantity": 2 },
    { "product": 7, "quantity": 1 }
  ]
}

