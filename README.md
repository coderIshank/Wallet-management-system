# Django Wallet & Transaction Ledger System

A backend wallet management system built using Django REST Framework (DRF).

This project allows users to:

- Register and login using JWT Authentication
- Create wallet
- Credit money
- Debit money
- Check wallet balance
- View transaction history
- Prevent duplicate transactions using idempotency
- Handle concurrent transactions safely

---

# Features

## Authentication
- User Registration
- JWT Login Authentication

## Wallet Management
- Create Wallet
- One Wallet per User
- Default balance = 0

## Transactions
- Credit Money
- Debit Money
- Prevent negative balance
- Transaction history with timestamps

## Idempotency
- Prevent duplicate transactions using unique transaction IDs

## Additional Features
- Pagination
- Date Filtering
- Unit Testing
- Proper API validations
- Proper HTTP status codes

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Programming Language |
| Django | Backend Framework |
| Django REST Framework | REST APIs |
| Simple JWT | Authentication |
| SQLite | Database |
| Postman | API Testing |

---

# Project Structure

```text
wallet_project/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── wallet/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
```

---

# Quick Start

```bash
git clone <your_repository_url>

cd wallet-system

python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

# Installation Steps

## 1. Clone Repository

```bash
git clone <your_repository_url>
```

Example:

```bash
git clone https://github.com/yourusername/wallet-system.git
```

---

## 2. Go To Project Directory

```bash
cd wallet-system
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv env
```

Activate virtual environment:

```bash
env\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv env
```

Activate virtual environment:

```bash
source env/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## 6. Run Development Server

```bash
python manage.py runserver
```

Server will start at:

```text
http://127.0.0.1:8000/
```

---

# Authentication

JWT Authentication is used.

After login, include token in headers:

```text
Authorization: Bearer your_access_token
```

---

# API Endpoints

# 1. Register User

## Endpoint

```text
POST /wallet/register/
```

## Request Body

```json
{
    "username": "ishank",
    "email": "ishank@gmail.com",
    "password": "123456"
}
```

## Success Response

```json
{
    "id": 1,
    "username": "ishank",
    "email": "ishank@gmail.com"
}
```

---

# 2. Login User

## Endpoint

```text
POST /wallet/login/
```

## Request Body

```json
{
    "username": "ishank",
    "password": "123456"
}
```

## Success Response

```json
{
    "refresh": "jwt_refresh_token",
    "access": "jwt_access_token"
}
```

---

# 3. Create Wallet

## Endpoint

```text
POST /wallet/create/
```

## Headers

```text
Authorization: Bearer access_token
```

## Success Response

```json
{
    "id": 1,
    "user": 1,
    "balance": "0.00"
}
```

---

# 4. Credit Money

## Endpoint

```text
POST /wallet/<wallet_id>/credit/
```

## Request Body

```json
{
    "amount": 1000,
    "transaction_id": "txn_101"
}
```

## Success Response

```json
{
    "message": "Money credited successfully.",
    "balance": "1000.00"
}
```

---

# 5. Debit Money

## Endpoint

```text
POST /wallet/<wallet_id>/debit/
```

## Request Body

```json
{
    "amount": 500,
    "transaction_id": "txn_102"
}
```

## Success Response

```json
{
    "message": "Money debited successfully.",
    "balance": "500.00"
}
```

---

# 6. Wallet Balance

## Endpoint

```text
GET /wallet/<wallet_id>/balance/
```

## Success Response

```json
{
    "wallet_id": 1,
    "balance": "500.00"
}
```

---

# 7. Transaction History

## Endpoint

```text
GET /wallet/<wallet_id>/transactions/
```

## Success Response

```json
[
    {
        "id": 1,
        "wallet": 1,
        "transaction_id": "txn_101",
        "transaction_type": "credit",
        "amount": "1000.00",
        "created_at": "2026-05-16T10:00:00Z"
    }
]
```

---

# Pagination

```text
GET /wallet/1/transactions/?page=1&limit=5
```

---

# Date Filtering

```text
GET /wallet/1/transactions/?start_date=2026-05-01&end_date=2026-05-15
```

---

# Idempotency

Duplicate transactions are prevented using unique transaction IDs.

If same transaction ID is sent multiple times:

```json
{
    "message": "Transaction already processed"
}
```

will be returned.

---

# Race Condition Handling

Race conditions are handled using:

```python
transaction.atomic()
```

and

```python
select_for_update()
```

This ensures:
- Safe concurrent transactions
- No incorrect balance updates

---

# Unit Tests

Unit tests are written using:
- Django TestCase
- DRF APITestCase

## Run Tests

```bash
python manage.py test
```

---

# Postman Collection

Postman collection is included in the project submission.

Import the collection into Postman to test APIs easily.

---

# Important Concepts Used

- Django REST Framework
- JWT Authentication
- DecimalField
- transaction.atomic()
- select_for_update()
- Idempotency
- Pagination
- Date Filtering
- Unit Testing

---

# Future Improvements

- Multiple wallets per user
- Redis caching
- Celery background tasks
- Docker support
- PostgreSQL database
- Swagger API documentation
- Rate limiting
- Async processing

---

# Author

Ishank Chauhan
