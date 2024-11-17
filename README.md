# efurniture

**efurniture** is an advanced e-commerce platform designed to streamline the process of buying and selling furniture
online. It features comprehensive management of products, orders, customers, and more, providing a seamless experience
for both customers and administrators.

## Contributing

- **[Phankong Samrach](https://github.com/pksrach)**
- **[Meas Manet](https://github.com/meas-manet)**

## Table of Contents

- [Contributing](#contributing)
- [Features](#features)
- [Core Functions](#core-functions)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Scripts Used](#scripts-used)
- [License](#license)

## Features

- **User Authentication**: Secure registration, login, and role-based access control.
- **Product Management**: Extensive catalog management with pricing, categories, and brands.
- **Order Processing**: Detailed order creation, tracking, and payment management.
- **Customer Profiles**: Manage customer details and order histories.
- **Staff Management**: Organize and manage staff assignments and roles.
- **Notifications**: Real-time notifications for order updates and promotions.
- **Responsive Design**: Optimized for a great experience on both desktop and mobile devices.

## Core Functions

### 1. User Management

- **User Registration and Login**: Secure authentication for users, including role-based access controls.
- **Profile Management**: Users can update their personal information, such as email and password.

### 2. Product Management

- **Product Catalog**: Manage inventory by adding, updating, and deleting products.
- **Product Pricing**: Set pricing based on attributes like color and size, and manage discounts.
- **Categories and Brands**: Organize products into categories and associate them with specific brands.
- **Product Ratings**: Allow customers to rate products, helping others with their purchasing decisions.

### 3. Order Management

- **Order Creation**: Facilitate order placement, including product selection and price calculation.
- **Order Details**: Manage specific order information, such as product quantities, pricing, and applied discounts.
- **Order Tracking**: Monitor order statuses, including payment processing and delivery tracking.

### 4. Customer Management

- **Customer Profiles**: Maintain detailed records of customer information, including contact details and linked user
  accounts.
- **Customer Orders**: Track customer orders and manage their status throughout the order lifecycle.

### 5. Payment Management

- **Payment Methods**: Support various payment methods with details like payment names and QR code attachments.
- **Order Payments**: Process and confirm payments for orders, and attach payment confirmations to orders.

### 6. Location Management

- **Location Listings**: Manage locations for product availability and delivery.
- **Location Pricing**: Adjust pricing based on location, such as shipping costs or regional pricing variations.

### 7. Notifications

- **User Notifications**: Send notifications between users, including order updates, promotions, and alerts.

### 8. Staff Management

- **Staff Profiles**: Manage staff information, including roles, contact details, and salary.
- **Staff Assignments**: Assign staff members to manage tasks such as order processing or customer support.

## Technology Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Frontend**: Next.js (React)
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: Docker, Vercel

## Installation

To set up the **efurniture** platform locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/pksrach/efurniture-backend.git
   cd efurniture

## API Documentation

- **[API Documentation](http://127.0.0.1:8000/docs)**

## Scripts Used

- **Create a virtual environment**:
  ```bash
  python -m venv venv
  ```

- **Activate the virtual environment**:
  ```bash
    source venv/Scripts/activate
    or
    source venv/bin/activate
    ```

- **Create a `.env` file**:
    ```bash
    touch .env
    ```

- **Add the following environment variables to the `.env` file**:
- **PG_HOST**=localhost
- **PG_PORT**=5432
- **PG_USER**=postgres
- **PG_PASSWORD**=postgres
- **PG_DB**=efurniture
- **SECRET_KEY**=your_secret_key


- **Install the required packages**:
  ```bash
  pip install -r requirements.txt
  ```
  
- **Initialize the database**:
  ```bash
  alembic init alembic
  ```

- **Generate database migration**:
  ```bash
  alembic revision --autogenerate -m "Initial migration"
  ```
  
- **Run the database migrations**:
  ```bash
  alembic upgrade heads
  ```

- **Run the FastAPI server**:
  ```bash
  uvicorn app.main:app --reload
  ```

## License

**[SS5 Group - SETEC Institute](https://www.setecu.com/)**

