# Coloshop

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)


## Introduction
Coloshop is an online shopping system for clothing. It offers a seamless shopping experience with features such as a cart, wishlist, product variants (color and size), multiple payment options, order tracking, and efficient return and refund processes.

## Features
- **Cart:** Easily add and manage items in your shopping cart.
- **Wishlist:** Save items for future purchase.
- **Variants:** Choose products based on color and size options.
- **Payment Integrations:** 
  - PayPal
  - Wallet
  - Cash on Delivery
- **Returns:** Users can return products after purchase and get refunds efficiently.
- **Order Tracking:** Users can track their orders in real-time.

## Installation
Follow these steps to get Coloshop up and running locally.

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/coloshop.git
   cd coloshop
2. **Set up a virtual environment::**
    python -m venv venv
    source venv/bin/activate 

3. **Install dependencies::**
    pip install -r requirements.txt

4. **Create and configure the .env file:**  

5. **Apply migrations::**
    python manage.py migrate

6. **Apply migrations::**
    python manage.py runserver

## Usage
Once the development server is running, open your web browser and navigate to http://127.0.0.1:8000/ to start using Coloshop. Register a new user or log in with an existing account to explore features like adding items to the cart, creating a wishlist, selecting product variants, and placing orders.    

## Environment Variables
Ensure you set the following environment variables in your .env file:
SECRET_KEY=django-insecure-23u*!o))a7!xcq%)ur0x^o#&axhro!=ydbu-_ar(c7r$gd@(hu
DEBUG=True
DATABASE_NAME=coloshop
DATABASE_USER=muhammedarfath
DATABASE_PASSWORD=1234
DATABASE_HOST=db
DATABASE_PORT=5432
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   




