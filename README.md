# Django REST API Documentation

This is the documentation for a Django REST API project that provides endpoints for managing bank accounts and transactions. Below you'll find instructions on how to set up the project and details about the available endpoints.

## Getting Started

Before you begin using the API, follow these steps to set up your development environment and ensure the project is properly configured.

### Create a Python 3 Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies with Poetry

We use [Poetry](https://python-poetry.org/) to manage Python dependencies. If you don't have it installed globally, you can install it within your virtual environment using pip:

```bash
pip install poetry
```

Install project dependencies:

```bash
poetry install
```

To add a new library to the project, use the following command:

```bash
poetry add [--dev] <library>
```

### Load Sample Data

To populate the database with sample data, run the following commands:

```bash
python manage.py migrate
python manage.py loaddata sample.json
```

This will create three users, including a superuser for the admin panel, along with bank accounts and transactions.

## Endpoints

The API provides the following endpoints for managing bank accounts and transactions:

- **List Accounts**: Get a list of all bank accounts.

  ```
  GET /accounts/
  ```

- **Retrieve Account**: Get details of a specific bank account by ID.

  ```
  GET /accounts/:id
  ```

- **List Transactions**: Get a list of all transactions with various filtering options.

  ```
  GET /transactions/
  ```

- **Retrieve Transaction**: Get details of a specific transaction by ID.

  ```
  GET /transactions/:id
  ```

## Authentication and Permissions

- Users can only see their own accounts and transactions.
- Admin users (defined by the `User.is_staff` flag) can view all accounts and transactions.

## Pagination

All list endpoints are paginated using cursor-based pagination.

## Filtering Transactions

The `transactions` endpoint allows you to filter transactions by:

- Start and/or end timestamp
- Account ID
- Transaction category (see `accounts.models.TransactionCategory`)

## Additional Account Fields

The `Account` endpoints include two fields not part of the normal `Account` model:

- `transaction_count_last_thirty_days`: The count of all transactions on this account in the last 30 days.
- `balance_change_last_thirty_days`: The sum of all transactions on this account in the last 30 days.

### Example Account Response

```json
{
    "id": 1,
    "user": 2,
    "name": "John Smith",
    "transaction_count_last_thirty_days": 119,
    "balance_change_last_thirty_days": "-1304.67"
}
```

### Example Transaction Response

```json
{
    "id": 1,
    "account": 1,
    "timestamp": "2022-06-12T17:36:58.632000Z",
    "amount": "-25.26",
    "description": "Tesco",
    "transaction_category": "PURCHASE"
}
```

Feel free to use this API documentation as a reference while working with the Django REST API project. If you have any questions or need further assistance, please don't hesitate to reach out.
