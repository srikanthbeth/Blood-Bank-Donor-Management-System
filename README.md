# 🩸 Blood Bank & Donor Management System

A complete **Blood Bank & Donor Management System** built using **FastAPI**, **SQLAlchemy**, **JWT Authentication**, and **SQLite**. This application manages blood donors, blood inventory, blood requests, donation history, and reporting with role-based access control.

---

# 🚀 Features

## Authentication & Authorization

- JWT Authentication
- User Registration
- User Login
- Password Hashing (bcrypt)
- Role-Based Access Control

### Roles

- Admin
- Staff
- Donor

---

# 📌 Modules

## 1. Authentication

### APIs

| Method | Endpoint | Description |
|----------|----------------|----------------|
| POST | `/auth/register` | Register User |
| POST | `/auth/login` | Login User |

---

## 2. Donor Management

### Features

- Add Donor
- View Donors
- Update Donor
- Delete Donor
- Search by Blood Group
- Search by City

### APIs

| Method | Endpoint |
|----------|----------------|
| POST | `/donors` |
| GET | `/donors` |
| GET | `/donors/{donor_id}` |
| PUT | `/donors/{donor_id}` |
| DELETE | `/donors/{donor_id}` |

---

## 3. Blood Inventory

### Features

- Add Blood Units
- View Inventory
- Update Inventory
- Expired Blood Validation

### APIs

| Method | Endpoint |
|----------|----------------|
| POST | `/inventory` |
| GET | `/inventory` |
| PUT | `/inventory/{inventory_id}` |

---

## 4. Blood Request Management

### Features

- Create Blood Request
- View Requests
- Approve Request
- Reject Request
- Complete Request
- Automatic Inventory Update

### APIs

| Method | Endpoint |
|----------|----------------|
| POST | `/requests` |
| GET | `/requests` |
| GET | `/requests/{request_id}` |
| PUT | `/requests/{request_id}` |

---

## 5. Donation History

### Features

- Record Donations
- View Donor Donation History
- Automatic Inventory Increase
- 90-Day Donation Validation

### APIs

| Method | Endpoint |
|----------|----------------|
| POST | `/donations` |
| GET | `/donations/my-history` |

---

## 6. Reports

### Features

- Search Donors by Blood Group
- Search Donors by City
- Filter Requests by Status
- Blood Stock Report
- Pagination Support

### APIs

| Method | Endpoint |
|----------|----------------|
| GET | `/reports/donors` |
| GET | `/reports/requests` |
| GET | `/reports/inventory` |

---

# 🔒 Business Rules

- A donor cannot donate again within **90 days**.
- Blood units cannot be issued if stock is insufficient.
- Expired blood units cannot be allocated.
- Inventory automatically increases after every donation.
- Inventory automatically decreases after request approval.
- Phone number must be unique.
- Donor age must be between **18 and 65**.
- Donors can only view their own donation history.
- Staff can manage Inventory and Requests.
- Admin can manage all modules.

---

# 🛠️ Technology Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Pytest

---

# 📂 Project Structure

```
blood_bank_donor_management_system/
│
├── routers/
│   ├── auth_router.py
│   ├── donor_router.py
│   ├── inventory_router.py
│   ├── request_router.py
│   ├── donation_router.py
│   └── report_router.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_donor.py
│   ├── test_inventory.py
│   ├── test_request.py
│   ├── test_reports.py
│   └── test_donation.py
│
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
├── config.py
├── requirements.txt
├── pytest.ini
├── blood_bank.db
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/blood_bank_donor_management_system.git
```

```bash
cd blood_bank_donor_management_system
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# 🧪 Run Tests

Run all tests:

```bash
pytest -v
```

Run a specific test:

```bash
pytest tests/test_auth.py -v
```

---

# 📖 API Testing

Use:

- Swagger UI
- Postman

---

# 🔑 Default Roles

- Admin
- Staff
- Donor

Create users using:

```
POST /auth/register
```

Login using:

```
POST /auth/login
```

Authorize in Swagger using:

```
Bearer <JWT Token>
```

---

# 📸 Screenshots

Include the following screenshots before submission:

- Swagger Home
- Register API
- Login API
- Donor APIs
- Inventory APIs
- Request APIs
- Donation APIs
- Reports APIs
- Pytest Results

---

# ✅ Validation

- JWT Authentication
- Role-Based Authorization
- Phone Number Validation
- Age Validation
- 90-Day Donation Rule
- Expired Blood Validation
- Stock Validation
- Pagination
- Search & Filtering

---

# 👨‍💻 Author

**Srikanth Bethamcharla**

---

# 📄 License

This project is developed for educational and learning purposes.
