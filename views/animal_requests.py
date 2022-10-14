import sqlite3
import json
# importing class Animals form models.animal.py
from models import Animal, Location, Customer
from .location_requests import get_single_location
from .customer_requests import get_single_customer 

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 4
    },
    {
        "id": 4,
        "name": "Eleanor",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    }
]

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        LEFT JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], 
                            row['name'], 
                            row['breed'],
                            row['status'], 
                            row['location_id'],
                            row['customer_id'])

            location = Location(row['location_id'],
                                row['location_name'],
                                row['location_address'])

            customer = Customer(row['customer_id'],
                                row['customer_name'],
                                row['customer_address'])

            animal.location = location.__dict__
            animal.customer = customer.__dict__

            animals.append(animal.__dict__)

    return animals

def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        LEFT JOIN Customer c
            ON c.id = a.customer_id
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(
                        data['id'], 
                        data['name'], 
                        data['breed'],
                        data['status'], 
                        data['location_id'],
                        data['customer_id'])

        location = Location(data['location_id'],
                            data['location_name'],
                            data['location_address'])

        customer = Customer(data['customer_id'],
                            data['customer_name'],
                            data['customer_address'])

        animal.location = location.__dict__
        animal.customer = customer.__dict__

        return animal.__dict__

def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal

def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        # The sql DELETE command only needs the "id"  or a target to delete the data.
        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], 
              new_animal['breed'],
              new_animal['status'], 
              new_animal['location_id'],
              new_animal['customer_id'], 
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

def get_animal_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], 
                            row['name'], 
                            row['breed'],
                            row['status'], 
                            row['location_id'],
                            row['customer_id'])

            animals.append(animal.__dict__)
        return animals













#? functions that have been udpdated
# # Function with a single parameter
# def get_single_animal(id):
#     # Variable to hold the found animal, if it exists
#     requested_animal = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for animal in ANIMALS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if animal["id"] == id:

#             # ~ return matching animals
#             requested_animal = animal

#             # ~ return matching locations along with animals
#             matching_location = get_single_location(requested_animal["locationId"])
#             requested_animal["location"] = matching_location

#             #* use del (delete) method to remove locationId key when a single animal is searched
#             del animal["locationId"]

#             # ~ return matching customers along with animals
#             matching_customer = get_single_customer(requested_animal["customerId"])
#             requested_animal["customer"] = matching_customer
            
#             #* use del (delete) method to remove customerId key when a single animal is searched
#             del animal["customerId"]


#     return requested_animal

# def delete_animal(id):
#     # Initial -1 value for animal index, in case one isn't found
#     animal_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Store the current index.
#             animal_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if animal_index >= 0:
#         ANIMALS.pop(animal_index)