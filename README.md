**Full-Featured E‑Commerce Platform (Saravex) – Complete Documentation**

---

## Table of Contents

1. Project Overview
2. Key Features
3. Technology Stack & Dependencies
4. Directory & File Structure
5. Data Storage & JSON Formats
6. Flask Application Configuration
7. Helper Functions

   * 7.1 `datas(filename)`
   * 7.2 `lod(key, raw_json)`
   * 7.3 `wri(filename, data)`
8. URL Routes & Endpoint Reference

   * 8.1 Home & Country Detection (GET `/`)
   * 8.2 Authentication Pages (`/login`, `/register`, `/logout`)
   * 8.3 Search & Category Browsing (`/searche_name`, `/cat_book`, `/catagory_i/<search_item>`)
   * 8.4 Product Detail & Slider (`/product/<record_id>`, `/test`, `/test1`)
   * 8.5 Seller Account Management (`/seller_account_intro`, `/get_seller_regi`)
   * 8.6 Product Upload & Management (`/product_up`, `/upload_product`)
   * 8.7 User Orders & Cart (`/add_to_cart/<p_id>`, `/your_orders`, `/confirm_order/<p_id>`, `/cancel_order/<p_id>`)
   * 8.8 Seller Orders (`/seller_order`)
   * 8.9 Static Pages (`/about_us`, `/contactus`, `/terms_and_condition`, `/faq`, `/privacy_policy`, `/return_policy`)
9. Template Structure & Frontend Overview
10. Static Assets & Upload Handling
11. Session Management & State
12. Input Validation & Security Considerations
13. Testing & Quality Assurance
14. Deployment & Production Setup
15. SEO Optimization & Keywords
16. Author & License

---

## 1. Project Overview

This is a **full-functioning e‑commerce platform** implemented with Flask. It supports product browsing, search, user registration/login, country-based personalization, cart and order handling, seller account creation, and order management. Data is persisted in lightweight JSON files (`regi`, `product`, `sellers`, `catagory`) and images under `static/img/product`.

---

## 2. Key Features

* **Geolocation**: Detect user country from IP and personalize content.
* **User Accounts**: Register, login, logout, profile, address book.
* **Product Catalog**: Browse by category, search by name or description.
* **Homepage Slider**: Display featured products in image carousel.
* **Cart & Orders**: Add to cart, view orders, confirm/cancel orders.
* **Seller Portal**: Register as seller, upload multiple product images, manage product listings.
* **Cart Counter**: Show number of items in cart.
* **Static Pages**: About, Contact, Terms, Privacy, FAQ, Return Policy.

---

## 3. Technology Stack & Dependencies

* **Python 3.8+**
* **Flask**: Web framework
* **Jinja2**: Templating engine
* **Requests**: External API calls (IP geolocation)
* **JSON**: Data serialization
* **Werkzeug**: File uploads
* **Bootstrap 5**: Responsive frontend (assumed)

**requirements.txt**:

```
Flask
requests
```

---

## 4. Directory & File Structure

```plaintext
ecommerce_app/
├── app.py                    # Main Flask application
├── templates/                # Jinja2 HTML templates
│   ├── home_image_slider.html
│   ├── login.html
│   ├── register.html
│   ├── product_main_page.html
│   ├── your_account.html
│   ├── your_addresses.html
│   ├── add_new_address.html
│   ├── seller_account_intro.html
│   ├── your_seller_account.html
│   ├── add_new_product.html
│   ├── home_image_slider.html
│   ├── product_search_page.html
│   └── select_payment_method.html
├── static/
│   └── img/
│       └── product/         # Product images
├── regi                      # User data (dict email→{name,passw,products,address})
├── sellers                   # Seller data (dict email→{business,products,order})
├── product                   # All product listings
├── catagory                  # Category→product IDs mapping
├── requirements.txt
└── README.md                 # Documentation
```

---

## 5. Data Storage & JSON Formats

### `regi` (Registered Users)

```json
{
  "alice@mail.com": {
    "name":"Alice",
    "email":"alice@mail.com",
    "passw":"pwd",
    "products": { /* cart items */ },
    "address": { /* address book */ }
  }
}
```

### `product` (Product Catalog)

```json
{
  "0.12345": {
    "titel":"Blue Lamp",
    "descip":"Stylish lamp",
    "price":"20",
    "discount":"5",
    "number":"10",
    "pic":["img/product/0.123451.jpg", ...],
    "seller":"Alice",
    "seller_email":"alice@mail.com"
  }
}
```

### `sellers` (Seller Profiles & Orders)

```json
{
  "bob@mail.com": {
    "email":"bob@mail.com",
    "business":"Bob’s Store",
    "business_description":"Best gadgets",
    "products": { /* IDs as keys */ },
    "order": { /* p_id→order details */ }
  }
}
```

### `catagory` (Category Index)

```json
{
  "electronics": { "0.12345": {/* product data */} },
  "books": { ... }
}
```

---

## 6. Flask Application Configuration

* **Upload Folder**: Configured at `/pictures`, actual saving in `static/img/product`.
* **Secret Key**: `app.secret_key` used for session.
* **Host & Port**: `app.run(host='0.0.0.0', port=5000, debug=True)` for development.

---

## 7. Helper Functions

### 7.1 `datas(filename)`

Reads and parses Python-literal files into Python dict with JSON normalization.

### 7.2 `lod(key, raw_json)`

Converts key + JSON string into a dict of form `{key: parsed_data}`.

### 7.3 `wri(filename, data)`

Writes Python dict back to file in literal string format.

---

## 8. URL Routes & Endpoint Reference

### 8.1 Home & Country Detection (GET `/`)

* Detect user country via IP-API
* Load category data to session: `cata`, `lip`, `dl`
* If logged in, load user cart and render `home_image_slider.html` with personalized context

### 8.2 Authentication

* **GET `/login`**: Render login page with category/session context
* **GET `/register`**: Render registration page
* **POST `/get_regi`**: Process registration, write to `regi`, set session, render home
* **POST `/get_login`**: Validate credentials, set session, redirect
* **GET `/logout`**: Clear session and render home

### 8.3 Search & Category Browsing

* **POST `/searche_name`**: Search by category or description substring; render `product_search_page.html`
* **POST `/cat_book`**: Fixed category “book” search
* **GET `/catagory_i/<search_item>`**: Browse specific category

### 8.4 Product Detail & Test Routes

* **GET `/product/<record_id>`**: Show detail page `product_main_page.html`
* **POST `/add_to_cart/<p_id>`**: Add product to user cart in `regi`
* **POST `/test`, `/test1`**: Debug endpoints

### 8.5 Seller Account Management

* **GET `/seller_account_intro`**: Intro or seller dashboard link
* **POST `/get_seller_regi`**: Register seller info in `sellers` and update `regi`

### 8.6 Product Upload & Management

* **GET `/product_up`**: Render `add_new_product.html`
* **POST `/upload_product`**: Handle four image uploads, append product data to `product`, `catagory`, `sellers`

### 8.7 User Orders & Cart

* **GET `/your_orders`**: Display user cart and total price
* **GET `/confirm_order/<p_id>`**: Render `select_payment_method.html` with saved addresses
* **GET `/cancel_order/<p_id>`**: Remove item from cart and update file

### 8.8 Seller Orders

* **GET `/seller_order`**: List all buyer orders for this seller

### 8.9 Static Pages

* **GET `/about_us`**, `/contactus`, `/terms_and_condition`, `/faq`, `/privacy_policy`, `/return_policy`
* Render corresponding templates with session context

---

## 9. Template Structure & Frontend Overview

Key templates under `templates/`:

* **home\_image\_slider.html**: Carousel, featured products
* **login.html** / **register.html**: Forms with Bootstrap
* **product\_main\_page.html**: Detailed product view
* **your\_account.html**, **your\_addresses.html**
* **add\_new\_address.html**, **seller\_account\_intro.html**, **your\_seller\_account.html**, **add\_new\_product.html**
* **product\_search\_page.html**: Search results
* **select\_payment\_method.html**: Checkout flow
* **your\_orders.html**, **seller\_order.html**
* Static includes: header, footer, navigation bar

---

## 10. Static Assets & Upload Handling

* **Image Uploads**: Saved to `static/img/product/` with unique IDs
* **CSS/JS**: Serve via `static/css/` and `static/js/`
* **Filenames** prefixed with product IDs to avoid collisions

---

## 11. Session Management & State

* **Flask Session** stores: `user`, `email`, `country`, `cata`, `lip`, `dl`, `cart`, `product`
* Used to persist user state across requests

---

## 12. Input Validation & Security Considerations

* **Form Validation**: Check required fields, match passwords
* **File Validation**: Ensure image MIME types
* **CSRF Protection**: Recommended (Flask-WTF)
* **Password Storage**: Currently plaintext; use hashing for production
* **XSS Mitigation**: Escape user input in Jinja2

---

## 13. Testing & Quality Assurance

* **Unit Tests**: For helper functions `datas`, `lod`, `wri`
* **Integration Tests**: Using Flask test client for form submissions and session flows
* **Manual Testing**: On mobile and desktop browsers

---

## 14. Deployment & Production Setup

1. **Install Requirements**: `pip install -r requirements.txt`
2. **Environment Variables**: Set `FLASK_ENV=production`
3. **WSGI Server**: `gunicorn app:app --bind 0.0.0.0:5000`
4. **Reverse Proxy**: Configure Nginx or Apache for SSL/TLS

---

## 15. SEO Optimization & Keywords

Include in `<head>`:

```html
<meta name="description" content="Shop electronics, books, home goods—responsive e-commerce site built with Flask.">
<meta name="keywords" content="Flask e-commerce, online shop, buy electronics, book store, seller portal, cart checkout">
```

**Suggested Keywords:**

```
Flask e-commerce platform
online shop Flask
product upload portal
seller dashboard Flask
cart and checkout
dynamic category browsing
geolocation personalization
Flask e-commerce platform
online shop Flask
product upload portal
seller dashboard Flask
cart and checkout
dynamic category browsing
geolocation personalization
```

---

## 16. Author & License

**Author:** Smaron Biswas
**Year:** 2023
**License:** MIT

Released under the MIT License—free to use, modify, and distribute.

---


