import sqlite3
import json
from models import Location

from operator import index


LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    # return CUSTOMERS   ~ old way to get all Customer without SQL integration
    #? Open a connection to the database (be sure to have correct path for sqlite3)
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        #~ conn.cursor - id a database cursor used to execute SQL statements and fetch results from SQL queries
        db_cursor = conn.cursor()

        # * SQL query - c abbrev for Customer table
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        #initialize empty list to hold response
        locations = []

        #convert rows of data into Python list
        dataset = db_cursor.fetchall()

        #iterate list of dataset  from fetchall()
        for row in dataset:

            location = Location(row['id'],
                                row['name'],
                                row['address'])

            locations.append(location.__dict__)

    return locations

# Function with a single parameter
def get_single_location(id):
    # return CUSTOMERS   ~ old way to get all Customer without SQL integration
    #? Open a connection to the database (be sure to have correct path for sqlite3)
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, ( id, ))

        #initialize empty list to hold response
        location = []

        #convert rows of data into Python list
        data = db_cursor.fetchone()

        location = Location(data['id'],
                            data['name'],
                            data['address'])

        return location.__dict__

# condensed function to create and add "id". Refer to animals_request.py for expanded explanation view.
def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location

def delete_location(id):
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
        if location_index >=0:
            LOCATIONS.pop(location_index)

def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break

def get_location_by_locationId(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id))

        locations = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__)
        return locations