# graintrack

This project is a REST API for an online store. It allows managing products, including operations such as retrieving product lists, filtering products by category, adding products, updating prices, setting discounts, reserving, selling, and generating sales reports

### Requirements
* Python 3.13
* Flask
* Flask SQLAlchemy
* Flask Migrate

### Setup
```bash
git clone https://github.com/s0nyseventeen/graintrack.git

cd graintrack
```

### Install dependencies

```bash
python3 -mvenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set up the database

Enter the python3 interpreter (type `python`) under the root folder. `venv` must be activated

```python
import src

app = src.create_app()

with app.app_context():
    src.db.create_all()
```

### Run the application:

```bash
flask --app src run --debug
```

### Authentication

This API uses JWT (JSON Web Token) for authentication. Users must obtain a token to access certain endpoints. The token is included in the `Authorization` header of each request

### How to Obtain a Token

To obtain a JWT, you need to authenticate a user. You can do this by sending a `POST` request to the login endpoint (for simplicity username and password is provided)

```bash
curl -X POST http://localhost:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin123"}'
```

Response

```json
{
    "token": "your_jwt_token"
}
```

## API Endpoints

#### Endpoints Requiring Authentication

After obtaining the JWT, you can include it in the Authorization header of subsequent requests to access protected endpoints. Here's how to make a request with the token using `curl`

```bash
curl -X GET http://localhost:5000/products/<endpoint> \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token"

```

1. Create a Product
Endpoint: `POST /products/create`. Description: Add a new product
    ```bash
    curl -X POST http://localhost:5000/products/create \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_jwt_token" \
    -d '{
        "name": "Product Name",
        "price": 10.0,
        "amount": 100,
        "category_id": 1
    }'
    ```

2. Update Product Price
Endpoint: PATCH `/products/<product_id>`. Description: Update the price of a product
    ```bash
    curl -X PATCH http://localhost:5000/products/product_id \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_jwt_token" \
    -d '{"price": 20.0}'
    ```

3. Set Discount
Endpoint: PATCH `/products/<product_id>/set_discount`. Description: Set a discount on a product
    ```bash
    curl -X PATCH http://localhost:5000/products/product_id/set_discount \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_jwt_token" \
    -d '{"discount": 20}'
    ```

4. Delete Product
Endpoint: DELETE `/products/<product_id>`. Description: Delete a product
    ```bash
    curl -X DELETE http://localhost:5000/products/product_id \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_jwt_token"
    ```

5. Sold Products Report
Endpoint: GET `/products/report`. Description: Generate a report of sold products, with optional category filter
    ```bash
    curl -X GET http://localhost:5000/products/report?category_id=<id> \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_jwt_token"
    ```

#### Endpoints which don't need Authentication

6. Get All Products Endpoint: GET `/products/all`. Description: Retrieve a list of all products
    ```bash
    curl -X GET http://localhost:5000/products/all -H "Content-Type: application/json"
    ```

7. Filter Products by Category Endpoint: GET `/products/filter?category_id=<id> `. Description: Filter products by category
    ```bash
    curl -X GET http://localhost:5000/products/filter?category_id=<id> -H "Content-Type: application/json"
    ``` 

8. Reserve Product
Endpoint: PATCH `/products/<product_id>/reserve`. Description: Reserve a product if it is not already reserved
    ```bash
    curl -X PATCH http://localhost:5000/products/<product_id>/reserve -H "Content-Type: application/json"
    ```

9. Unreserve Product
Endpoint: PATCH `/products/<product_id>/unreserve`. Description: Unreserve a product if it is currently reserved
    ```bash
    curl -X PATCH http://localhost:5000/products/<product_id>/unreserve -H "Content-Type: application/json"
    ```

10. Sell Product
Endpoint: PATCH `/products/<product_id>/sell`. Description: Mark a product as sold if it has not already been sold
    ```bash
    curl -X PATCH http://localhost:5000/products/<product_id>/sell -H "Content-Type: application/json"
    ```