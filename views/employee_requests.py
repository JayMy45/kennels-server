import sqlite3
import json
from models import Employee, Location

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
            e.location_Id,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id
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

            location = Location(row['location_id'],
                                row['location_name'],
                                row['location_address'])

            
            employee.location = location.__dict__

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
            emp.location_Id,
            l.name location_name,
            l.address location_address
        FROM Employee emp
        JOIN Location l
            ON l.id = emp.location_id
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

        location = Location(data['location_id'],
                            data['location_name'],
                            data['location_address'])

        employee.location = location.__dict__
                            
        return employee.__dict__


def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id )
        VALUES
            ( ?, ?, ?);
        """, (new_employee['name'], 
              new_employee['address'], 
              new_employee['location_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id
        
    return new_employee

def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                location_Id = ?
        WHERE id = ?
        """, (new_employee['name'], 
              new_employee['address'],
              new_employee['location_Id'],
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


def get_employee_by_employeeId(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            emp.id,
            emp.name,
            emp.address,
            emp.location_Id,
            l.name location_name,
            l.address location_address
        FROM Employee emp
        WHERE emp.id = ?
        """, ( id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_Id'])
            employees.append(employee.__dict__)
        return employees