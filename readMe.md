# Inventory Management System

A web-based Inventory Management System developed using **Python Flask, MySQL, HTML, CSS, and Bootstrap/CSS styling**. The system helps small businesses manage product records, monitor stock levels, and keep track of inventory value.

## Features

Add new products.
View all registered products.
Update existing product information.
Delete discontinued products.
Search products by name, category, or supplier.
Identify products with low stock levels.
View total products, low-stock items, and inventory value.

## Technologies Used

Backend: Python, Flask
Database: MySQL
Frontend: HTML, CSS
Database Connector: MySQL Connector/Python
Environment Variables: python-dotenv

## Installation and Setup

### 1. Clone the Repository

Open your terminal or PowerShell and run:

git clone https://github.com/ecwebtestings-dev/inventory.git

### 2. Navigate to the Project Directory

cd inventory


### 3. Create a Virtual Environment
python -m venv venv

### 4. Activate the Virtual Environment

**Windows PowerShell:**

\venv\Scripts\Activate

5. Install Dependencies

pip install -r requirements.txt


6. Create the MySQL Database

CREATE DATABASE inventory_db;


**Important:** If the project contains a database SQL file, import it into `inventory_db` to create the required tables and structure. Otherwise, create the required product table according to the application's database schema.

### 7. Configure Environment Variables

Create a `.env` file in the root directory of the project, where `app.py` is located.

Add the following configuration:
SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_db

### 8. Run the Application

Start the Flask development server:
python app.py


### 9. Open the Application

Open your browser and visit:

http://127.0.0.1:5000/


The Inventory Management System should now be running locally.

## Project Structure

inventory/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_product.html
│   ├── edit_product.html
│   │
│   └──product_fields.html
│
└── static/
    └── style.css

*The structure above illustrates the expected project organization. Actual files may vary.*

## Troubleshooting

**1. MySQL connection error**

Ensure MySQL Server is running.
Check your database name, username, and password in `.env`.
Confirm that the `inventory_db` database exists.

**2. Module not found error**

Run:
pip install -r requirements.txt
