# MediPay

This repository includes a basic test suite developed as part of a **Software Testing** university course. The objective of the assignment was to practice writing unit tests for a Python desktop application, understand the fundamentals of software testing, and verify the correctness of core application functionality.

The tests were written using Python's built-in **unittest** framework and focus on validating database operations and the application's business logic.

> **Note:** This is an educational project created for learning software testing concepts rather than a production-ready testing solution.


MediPay is a desktop-based medical payment management application developed using **Python**, **Tkinter**, and **SQLite**.

This project was developed as a university assignment to practice desktop application development, database management, and GUI programming using Python.

---

## Features

- User registration
- User login
- Deposit money
- Purchase products
- Automatic 10% service fee calculation
- Transaction history
- Balance calculation
- Product invoice generation
- SQLite database storage

---

## Technologies

- Python
- Tkinter
- SQLite3

---

## Database Structure

The application uses four main tables:

| Table | Purpose |
|--------|---------|
| `users` | Stores user accounts |
| `products` | Stores purchased products |
| `Deposit_user` | Stores deposit transactions |
| `Whithdraw_user` | Stores withdrawal transactions |

---

## Application Workflow

1. Register a new account.
2. Login using your credentials.
3. Deposit funds into your account.
4. Purchase products.
5. View payment history.
6. Generate product invoices.

---

## Main Functionalities

### Authentication

- User registration
- User login
- Duplicate username validation

### Deposit

Users can add money to their account. Every deposit is stored together with:

- Amount
- Date
- Time

---

### Product Purchase

When purchasing a product:

- Product information is stored.
- A 10% service fee is automatically calculated.
- The total cost is deducted from the user's balance.

---

### Payments

The application displays:

- Deposit history
- Withdrawal history
- Current account balance

---

### Invoice Generation

Users can generate a simple invoice for any purchased product.

The invoice is exported as a text file containing:

- Product ID
- Product Name
- Product Price
- User ID

---

## Notes

This project was created for educational purposes and focuses on learning:

- Python GUI programming
- SQLite database operations
- Desktop application development
- Basic software architecture


# Software Testing

## Overview

This directory contains the automated tests developed for the **MediPay** project.

The test suite was created as part of a **Software Testing** university assignment with the objective of learning the fundamentals of unit testing, database testing, and basic GUI testing in Python.

The tests are implemented using Python's built-in `unittest` framework and primarily focus on validating database operations and application logic.

> **Note:** These tests were developed for educational purposes and are intended to demonstrate software testing concepts rather than provide production-level test coverage.

---

## Technologies

- Python
- unittest
- SQLite
- unittest.mock

---

## Test Files

| File | Description |
|------|-------------|
| `test_medipay.py` | Tests the main MediPay application including authentication features. |
| `test_mypay.py` | Tests the administrator dashboard, database queries, and GUI-related functionality. |

---

# test_medipay.py

This test module validates the core authentication functionality of the MediPay application.

## Covered Scenarios

### User Registration

The following cases are tested:

- Successful account registration
- Registration with an existing username

---

### User Login

The following scenarios are verified:

- Login using valid credentials
- Login using invalid credentials

---

### Database Testing

The tests use an isolated SQLite in-memory database to verify that user records are inserted and retrieved correctly.

---

# test_mypay.py

This module focuses on validating the administrator dashboard logic and SQL queries.

## Covered Scenarios

### User Balance Calculation

Verifies that user balances are calculated correctly using deposits and withdrawals.

```
Balance = Total Deposits − Total Withdrawals
```

---

### Product Retrieval

Checks that products stored in the database can be retrieved successfully.

---

### Payment History

Verifies that:

- Deposit records are returned correctly.
- Withdrawal records are returned correctly.

---

### Invoice Lookup

Tests retrieving a product using its Product ID and User ID before invoice generation.

---

### GUI Testing

A basic GUI test verifies that Tkinter windows can be created successfully without runtime errors.

---

## Test Database

To avoid modifying the real application database, the tests use an SQLite in-memory database.

```python
sqlite3.connect(":memory:")
```

A fresh database is created before each test and automatically removed after the test completes.

---

## Test Isolation

Each test follows the standard `unittest` lifecycle:

- `setUp()` creates a temporary database and inserts sample data.
- `tearDown()` closes the database connection after each test.

This ensures that every test runs independently.

---

## Mocking

Some experimental tests (currently commented out) demonstrate the use of Python's `unittest.mock` module to mock:

- Tkinter windows
- Treeview widgets
- Message boxes
- Database cursor interactions

These tests were created as part of learning how mocking can isolate GUI components from application logic.

---

## Running the Tests

Run the MediPay tests:

```bash
python test_medipay.py
```

Run the MyPay tests:

```bash
python test_mypay.py
```

---

## Limitations

Because this project was developed for a university Software Testing course, the test suite has several limitations:

- Limited GUI automation
- No integration testing
- No end-to-end testing
- No performance testing
- No code coverage analysis
- Limited edge-case validation

---

## Learning Objectives

This test suite was created to gain practical experience with:

- Unit Testing
- Database Testing
- SQL Query Validation
- Test Isolation
- Mock Objects
- Basic GUI Testing
- Software Testing using Python's `unittest` framework
