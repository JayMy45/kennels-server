import sqlite3
import json
from models import Customer

CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay"
    }
]

def get_all_customers():
    # return CUSTOMERS   ~ old way to get all Customer without SQL integration
    #? Open a connection to the database (be sure to have correct path for sqlite3)
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # * SQL query - c abbrev for Customer table
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        """)

        #initialize empty list to hold response
        customers = []

        #convert rows of data into Python list
        dataset = db_cursor.fetchall()

        #iterate list of dataset  from fetchall()
        for row in dataset:

            customer = Customer(row['id'],
                                row['name'],
                                row['address'],
                                row['email'],
                                row['password'])

            customers.append(customer.__dict__)

    return customers


# Function with a single parameter
def get_single_customer(id):
    # Variable to hold the found customer, if it exists
    requested_customer = None

    # Iterate the CUSTOMERS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer

def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    return customer

# condensed code...refer to animal_request for details
def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index
        if customer_index >= 0:
            CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break