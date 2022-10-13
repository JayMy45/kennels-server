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
# * for details of function refer to animal_requests get_single_animal()
def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """,  ( id, ))

        customer = []

        data = db_cursor.fetchone()

        # since only one point of data will be requested
        # and there is no iterator data is used directly as 
        # instead of row as seen above as it (row) iterated the dataset there.
        customer = Customer(data['id'],
                            data['name'],
                            data['address'],
                            data['email'],
                            data['password'])
        # no need to append the dataset as only on row is represented
        # therefore the captured data can be returned directly
        
    return customer.__dict__

def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    new_id = max_id + 1
    customer["id"] = new_id
    CUSTOMERS.append(customer)
    return customer

# condensed code...refer to animal_request for details
def delete_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM customer
        WHERE id = ?
        """, (id, ))

def update_customer(id, new_customer):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Customer
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?
        WHERE id = ?
        """, (new_customer['name'], 
              new_customer['address'],
              new_customer['email'], 
              new_customer['password'],
              id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
    # Forces 404 response by main module
        return False
    else:
    # Forces 204 response by main module
        return True

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email,))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers
#! added this function to see how two separate search parameters would work...>
def get_customers_by_name(name):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.name = ?
        """, ( name,))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers











#! First iteration of get_single_customer() function.  So see matching refer to animal_request.py file (bottom)
# def get_single_customer(id):
#     # Variable to hold the found customer, if it exists
#     requested_customer = None

#     # Iterate the CUSTOMERS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for customer in CUSTOMERS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if customer["id"] == id:
#             requested_customer = customer

#     return requested_customer