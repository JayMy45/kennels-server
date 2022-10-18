import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animal_by_status
from views import get_all_employees, get_single_employee, create_employee, delete_employee, update_employee, get_employee_by_employeeId
from views import get_all_locations, get_single_location, create_location, delete_location, update_location, get_location_by_locationId
from views import get_all_customers, get_single_customer, create_customer, delete_customer, update_customer, get_customers_by_email, get_customers_by_name


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.

class HandleRequests(BaseHTTPRequestHandler):

    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # self._set_headers(200)

        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

         # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                    if response is not None:
                        self._set_headers(200)  
                    else:
                        self._set_headers(404)          
                        response = { "message": f"Animal {id} is out playing right now" } 
                else:
                    self._set_headers(200)
                    response = get_all_animals()

            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {"message": f"Location {id} is not open"}
                else:
                    self._set_headers(200)
                    response = get_all_locations()

            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {"message": f"Employee {id} does not exist"}
                else:
                    self._set_headers(200)
                    response = get_all_employees()

            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {"message": f"Customer {id} does not exist"}
                else:
                    self._set_headers(200)
                    response = get_all_customers()
        
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                self._set_headers(200)
                response = get_customers_by_email(query['email'][0])

            elif query.get('name') and resource == 'customers':
                self._set_headers(200)
                response = get_customers_by_name(query['name'][0])

            elif query.get('id') and resource == 'locations':
                self._set_headers(200)
                response = get_location_by_locationId(query['id'][0])
            
            elif query.get('id') and resource == 'employees':
                self._set_headers(200)
                response = get_employee_by_employeeId(query['id'][0])

            elif query.get('status') and resource == 'animals':
                self._set_headers(200)
                response = get_animal_by_status(query['status'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_employee = None
        new_customer = None
        new_location = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            if "name" in post_body:
                self._set_headers(201)
                new_animal = create_animal(post_body)
            else:
                self._set_headers(400)
                new_animal = { "message": f'{"Name is required" if "name" not in post_body else ""} {"Species is required" if "species" not in post_body else ""} {"locationId is required" if "locationId" not in post_body else ""} {"customerId is required" if "customerId" not in post_body else ""}'}
            self.wfile.write(json.dumps(new_animal).encode())

        # Add a new employee to the list.
        if resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_employee = create_employee(post_body)

            else:
                self._set_headers(400)
                new_employee = { "message": f'{"Name is required" if "name" not in post_body else ""}'}
            self.wfile.write(json.dumps(new_employee).encode())
        
        if resource == "customers":
            if "name" in post_body:
                self._set_headers(201)
                new_customer = create_customer(post_body)

            else:
                self._set_headers(400)
                new_customer = { "message": f'{"Name is required" if "name" not in post_body else ""}'}
            self.wfile.write(json.dumps(new_customer).encode())
        
        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create_location(post_body)
                
            else:
                self._set_headers(400)
                new_location = { "message": f'{"address is required" if "address" not in post_body else ""}{"Name is required" if "name" not in post_body else ""}'}
            self.wfile.write(json.dumps(new_location).encode())
        # Encode the new animal and send in response

    # A method that handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        # Encode the new animal and send in response
        self.wfile.write("".encode())

        #Encode the new employees and send in response
        if resource == "employees":
            success = update_employee(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())

        #Encode the new locations and send in response
        if resource == "locations":
            success = update_location(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())
      
        #Encode the new locations and send in response
        # if resource == "customers":
        #     success = update_customer(id, post_body)
        #     if success:
        #         self._set_headers(204)
        #     else:
        #         self._set_headers(404)
        # self.wfile.write("".encode())
  

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # * DELETE METHOD 
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)
        # self._set_headers(405)


        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        #* customer needs to contact company to have data deleted
        #* so need to send an message along with status (405) Method Not Allowed
        #* first initialize response

        response = None
      

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            self.wfile.write("".encode())
            #customers no longer able to delete animals directly...
            # response initialized above...
            #~ response = { "message": f"Deleting animals requires contacting the company directly"}
            
            # delete_animal(id)
            self.wfile.write(json.dumps(response).encode())
        
        # Delete a single customer from list
        # ? has to have a separate wfile line.
        if resource == "customers":
            delete_customer(id)
            # response = { "message": f"Deleting customers data requires contacting the company directly"}
            self.wfile.write(json.dumps(response).encode())
       
        # Delete a single location from list
      
        if resource == "locations":
            delete_location(id)
            # response = { "message": f"Deleting location data requires contacting the company directly"}
            self.wfile.write(json.dumps(response).encode())

        # Delete a single employee from list
        if resource == "employees":
            delete_employee(id)
            # response = { "message": f"Deleting employees data requires contacting the company directly"}
            self.wfile.write(json.dumps(response).encode())

        #* example of working code to delete an employee using the delete_employee() function
        # if resource == "employees":
        #     delete_employee(id)

        # self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
