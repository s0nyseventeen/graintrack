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

### Run migrations to set up the database

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

## API Endpoints

1. Create a Product
Endpoint: `POST /products/create`. Description: Add a new product
    ```json
    {
        "name": "Product Name",
        "price": 10.0,
        "category_id": 1
    }
    ```

2. Get All Products Endpoint: GET `/products/all`. Description: Retrieve a list of all products

3. Filter Products by Category Endpoint: GET `/products/filter?category_id=<id> `. Description: Filter products by category

4. Update Product Price
Endpoint: PATCH `/products/<product_id>`. Description: Update the price of a product
    ```json
    {
        "price": 20.0
    }
    ```

5. Set Discount
Endpoint: PATCH `/products/<product_id>/set_discount`. Description: Set a discount on a product
    ```json
    {
        "discount": 15.0
    }
    ```

6. Reserve Product
Endpoint: PATCH `/products/<product_id>/reserve`. Description: Reserve a product if it is not already reserved

7. Unreserve Product
Endpoint: PATCH `/products/<product_id>/unreserve`. Description: Unreserve a product if it is currently reserved

8. Sell Product
Endpoint: PATCH `/products/<product_id>/sell`. Description: Mark a product as sold if it has not already been sold

9. Delete Product
Endpoint: DELETE `/products/<product_id>`. Description: Delete a product

10. Sold Products Report
Endpoint: GET `/products/report?category_id=<id>`. Description: Generate a report of sold products, with optional category filter