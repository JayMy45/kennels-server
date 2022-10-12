import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    },
]

def get_all_employees():
    # return Employees   ~ old way to get all Customer without SQL integration
    #? Open a connection to the database (be sure to have correct path for sqlite3)
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # * SQL query - c abbrev for Customer table
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_Id
        FROM employee e
        """)

        #initialize empty list to hold response
        employees = []

        #convert rows of data into Python list
        dataset = db_cursor.fetchall()

        #iterate list of dataset  from fetchall()
        for row in dataset:

            employee = Employee(row['id'],
                                row['name'],
                                row['address'],
                                row['location_Id'])

            employees.append(employee.__dict__)

    return employees

# Function with a single parameter
def get_single_employee(id):
    # return CUSTOMERS   ~ old way to get all Customer without SQL integration
    #? Open a connection to the database (be sure to have correct path for sqlite3)
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            emp.id,
            emp.name,
            emp.address,
            emp.location_Id
        FROM employee emp
        WHERE emp.id = ?
        """, ( id, ))

        #initialize empty list to hold response
        data = []

        #convert rows of data into Python list
        data = db_cursor.fetchone()

        employee = Employee(data['id'],
                            data['name'],
                            data['address'],
                            data['location_Id'])

        return employee.__dict__


def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    #  Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
        if employee_index >=0:
            EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break 