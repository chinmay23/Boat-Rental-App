from a import DBbase, BoatCustomer, BoatPrice, BoatKind, BoatInventory, BoatAdmin
#from tabulate import tabulate

'''
<><03/14/2022>
Below is the base class Person holding  details between Customer and Admin class
'''
class Person():
    def __init__(self, name, city, state):
        self.name = name
        self.city=city
        self.state = state

'''
<><03/14/2022>
Below is the Customer class holding details about the customers
Methods in this class  interact with the BoatCustomer table in the db. 
A customer can be added, deleted using the methods from this class. 
'''
class Customer(Person):
    def __init__(self, name=None, city=None, state=None, identity=None):
        super().__init__(name, state)
        self.cust_identity = identity

    # Adds customer to BoatCustomer table in db
    def add_customer(self):
        BoatCustomer().add(self.name, self.city,self.state, self.cust_identity)

    '''
    Gets  boats that are available for reservation from database
    INPUT: 
        reserved_flag: getting details of all boats with reserved_flag status passed as parameter. 
    
    '''
    def get_boats_for_customer(self, reserved_flag):
        try:
            has_data = False
            db = DBbase("BoatRental.sqlite")
            db.connect()
            boat_list = db.get_cursor.execute("""
                                                SELECT BoatInventory.boat_make, BoatInventory.boat_id, BoatKind.boat_kind, BoatPrice.boat_price
                                                FROM BoatInventory
                                                INNER JOIN BoatType
                                                 ON BoatInventory.boat_id = BoatKind.boat_id
                                                 INNER JOIN BoatPrice
                                                    ON BoatKind.boat_id = BoatPrice.boat_id
                                                WHERE BoatInventory.reserved_flag = ?
                                                ORDER BY BoatInventory.boat_id;
                                                    """, (reserved_flag,))
            db.get_connection.commit()
            for item in boat_list:
                print(item)
                has_data = True
            if has_data:
                print("List of boats not reserved are fetched")
            else:
                print("All boats are reserved")
        except Exception as e:
            print("Error: Couldn't get boats", e)
        finally:
            db.close_db()

    '''
   Below function gets all boats prices 
    
    '''

    def get_boat_price (self, boat_model):
        try:
            has_data = False
            price = 0
            db = DBbase("BoatRental.sqlite")
            db.connect()
            boat_price = db.get_cursor.execute("""
                                                SELECT BoatPrice.boat_price
                                                from BoatPrice
                                                WHERE BoatPrice.boat_id = (SELECT BoatInventory.boat_id
                                                                           from BoatInventory
                                                                           where BoatInventory.boat_make = ?
                                                                          )
                                                    """, (boat_make,))
            db.get_connection.commit()
            for item in boat_price:
                price = item
                has_data = True
            if has_data:
                print("Amount:${} to be paid".format(price[0]))
            else:
                print("Couldn't find price for this Boat make")
        except Exception as e:
            print("Error: Couldn't find price", e)
        finally:
            db.close_db()

    def get_boats_reserved_by_customer(self, customer_id):
        try:
            has_data = False
            db = DBbase("BoatRental.sqlite")
            db.connect()
            boat_list = db.get_cursor.execute("""
                                                SELECT BoatInventory.boat_make, BoatInventory.boat_id, BoatKind.boat_kind, BoatPrice.boat_price
                                                FROM BoatInventory
                                                INNER JOIN BoatType
                                                 ON BoatInventory.boat_id = BoatKind.boat_id
                                                 INNER JOIN BoatPrice
                                                    ON BoatKind.boat_id = BoatPrice.boat_id
                                                WHERE BoatInventory.reserved_flag = 'Y' AND BoatInventory.cust_id = ?
                                                ORDER BY BoatInventory.boat_id;
                                                    """, (cust_id,))
            db.get_connection.commit()
            for item in boat_list:
                print(item)
                has_data = True
            if has_data:
                print("Boats reserved for the customer were fetched")
            else:
                print("No boats reserved")
        except Exception as e:
            print("Error: Couldn't retrieve boats reserved", e)
        finally:
            db.close_db()

    '''
    Reserves a particular boat make for customer in the database.
    
    boat_make: model number customer has want to reserve.
    cust_id: id of customer wanting the reservation.
    '''
    def reserve_boat_for_customer(self, boat_make, cust_id):
        try:
            d = BoatInventory().fetch(boat_make=boat_make)
            if d is None:
                print("Incorrect boat make number entered")
            else:
                if 'Y' in d:
                    print("The boat is reserved, enter other boat make number")
                else:
                    BoatInventory().update(boat_make, reserved_flag='Y', cust_id=cust_id)
                    print("Boat reserved for customer : {}!".format(cust_id))

        except Exception as e:
            print("Error: Couldn't reserve boat", e)

    '''
    Cancels any reservation if customer want to. 
    boat_make: Make number customer has reserved earlier or want to cancel the reservation of.
    cust_id: id of customer cancelling the reservation.
    '''
    def cancel_boat_for_customer(self, boat_make, cust_id):
        try:
            d = BoatInventory().fetch(boat_make=boat_make)
            if d is None:
                print("Incorrect boat make number")
            else:
                if 'Y' in d:
                    if cust_id in d:
                        BoatInventory().update(boat_make, reserved_flag='N', cust_id=0)
                        print("Reservation cancelled : {}!".format(cust_id))
                    else:
                        print("Boat reserved not under your name. Enter the make number reserved by you")
                else:
                    print("Boat not reserved. Enter the make number reserved by you")

        except Exception as e:
            print("Error: Unable to get boats for customer", e)

    '''
    Customer returns the boat. We need to make that available in inventory again.
    boat_make: make number of boat customer want to return.
    cust_id: id of customer returning the boat. 
   
    '''
    def return_boat_for_customer(self, boat_make, cust_id):
        try:
            d = BoatInventory().fetch(boat_make=boat_make)
            if d is None:
                print("Incorrect boat make number")
            else:
                if 'Y' in d:
                    if cust_id in data:
                        BoatInventory().update(boat_make, reserved_flag='N', cust_id=0)
                        print("Boat make {} returned by customer: {}!".format(boat_make, cust_id))
                        self.get_boat_price(boat_make=boat_make)
                    else:
                        print("Boat make number not reserved under your name. Enter the boat make you purchased to return")
                else:
                    print("Boat make not reserved. Enter the boat make you purchased to return")

        except Exception as e:
            print("Error: Couldn't return boat for customer", e)

    '''
    Based on the customer selection, this function calls the respective methods to update the database.
    
    cust_selection: Selection made by customer. 
    
    '''
    def update_database(self, customer_selection):
        if customer_selection == 1:
            self.get_boats_for_customer('N')
        elif customer_selection == 2:
            customer_id = int(input("Enter your customer id: "))
            self.get_boats_reserved_by_customer(cust_id)
        elif customer_selection == 3:
            cust_id = int(input("Enter your customer id: "))
            boat_make = input("Enter Boat make number: ")
            self.reserve_boat_for_customer(boat_make=boat_make, cust_id=cust_id)
        elif customer_selection == 4:
            cust_id = int(input("Enter your customer id: "))
            boat_make = input("Enter boat make number: ")
            self.cancel_boat_for_customer(boat_make=boat_make, cust_id=cust_id)
        elif customer_selection == 5:
            cust_id = int(input("Enter your customer id: "))
            boat_make = input("Enter boat make: ")
            self.return_boat_for_customer(boat_make=boat_make, cust_id=cust_id)

'''
Below is the Admin class holding details about the admin
There are methods in this class that interact with the BoatAdmin table in the database.
A admin can be added, deleted using the methods from this class. 
'''
class Admin(Person):
    def __init__(self, name=None, state=None, password=None):
        super().__init__(name, state)
        self.password = password

    # Adds admin to BoatCustomer table in db
    def add_admin(self):
        BoatAdmin().add(self.name,self.state, self.password)

    '''
    Based on the Admin's selection, this function calls the respective methods to update the database.
    
    top_level_option: selection of which table admin wants to update.
    detail_level_option:  selection of what action admin wants to take on selected table
    '''
    def update_database(self, top_level_option, detail_level_option):
        if detail_level_option == 1:
            if top_level_option == 1:
                print(BoatInventory().fetch())
            elif top_level_option == 2:
                print(BoatCustomer().fetch())
            elif top_level_option == 3:
                print(BoatKind().fetch())
            elif top_level_option == 4:
                print(BoatPrice().fetch())
            elif top_level_option == 5:
                print(BoatAdmin().fetch())
        elif detail_level_option == 2:
            if top_level_option == 1:
                boat_make = input("Enter the boat make: ")
                boat_id = int(input("Enter the boat id: "))
                reserved_flag = input("Enter if the boat is reserved (Y/N): ")
                cust_id = int(input("Enter the customer ID (0/ID): "))
                BoatInventory().add(boat_make, boat_id, reserved_flag, cust_id)

            elif top_level_option == 2:
                cust_name = input("Enter the customer name: ")
                cust_city = input("Enter city of the customer: ")
                cust_state = input("Enter the state of the customer: ")
                cust_identity = input("Enter the customer identification number: ")
                BoatCustomer().add(cust_name,cust_city, cust_state,cust_identity)

            elif top_level_option == 3:
                boat_id = int(input("Enter the boat id: "))
                boat_name = input("Enter the kind of boat: ")
                BoatKind().add(boat_id, boat_name)

            elif top_level_option == 4:
                boat_id = int(input("Enter the boat id: "))
                boat_price = int(input("Enter the boat price: "))
                BoatPrice().add(boat_id, boat_price)

            elif top_level_option == 5:
                admin_name = input("Enter the admin name: ")
                admin_state = input("Enter the state of the admin: ")
                admin_password = input("Enter the password of the admin: ")
                BoatAdmin().add(admin_name, admin_state, admin_password)

        elif detail_level_option == 3:
            if top_level_option == 1:
                boat_make = input("Enter the boat make number: ")
                boat_id = int(input("Enter the boat id: "))
                reserved_flag = input("Enter if the boat is reserved (Y/N): ")
                cust_id = int(input("Enter the customer ID: "))
                BoatInventory().update(boat_make, boat_id, reserved_flag, cust_id)

            elif top_level_option == 2:
                cust_id = int(input("Enter the customer ID: "))
                cust_name = input("Enter the name of the customer: ")
                cust_city = input("Enter the city of the customer: ")
                cust_state = input("Enter the state of the customer: ")
                cust_identity = input("Enter the customer identification number: ")
                BoatCustomer().update(cust_id, cust_name, cust_state, cust_identity)

            elif top_level_option == 3:
                boat_id = int(input("Enter the boat id: "))
                boat_kind = input("Enter the kind of boat: ")
                BoatKind().update(boat_id, boat_kind)

            elif top_level_option == 4:
                boat_id = int(input("Enter the boat id: "))
                boat_price = int(input("Enter the boat price: "))
                BoatPrice().update(boat_id, boat_price)

            elif top_level_option == 5:
                admin_id = int(input("Enter the admin ID: "))
                admin_name = input("Enter the admin name: ")
                admin_state = input("Enter the admin state: ")
                admin_password = input("Enter the admin password: ")
                BoatAdmin().update(admin_id, admin_name, admin_state, admin_password)

        elif detail_level_option == 4:
            if top_level_option == 1:
                boat_make = input("Enter the boat make number: ")
                BoatInventory().delete(boat_make)

            elif top_level_option == 2:
                customer_id = int(input("Enter the customer ID: "))
                BoatCustomer().delete(customer_id)

            elif top_level_option == 3:
                boat_id = int(input("Enter the boat id: "))
                BoatKind().delete(boat_id)

            elif top_level_option == 4:
                boat_id = int(input("Enter the boat id: "))
                BoatPrice().delete(boat_id)

            elif top_level_option == 5:
                admin_id = int(input("Enter the admin ID: "))
                BoatAdmin().delete(admin_id)

def format_options(dict_data):
    print('---')
    print("{:<8} {:<15}".format('Options', 'Description'))
    for k, v in dict_data.items():
        label = v
        print("{:<8} {:<15}".format(k, label))

if __name__ == '__main__':
    print("Welcome to Panama boat services! \n Prices per boat you see are prices for entire day\n")
    while True:
        interacting_person = int(input("Enter 1 for Admin. 2 for Customer. 3 for exiting the program: "))
        #For admin
        if interacting_person == 1:
            while True:
                admin_status = int(input("Are you new admin or existing admin? \n Enter 1 for new or 2 for existing or 3 for exiting the program: "))

                #New admin:
                if admin_status == 1:
                    name = input("Enter your username: ")
                    state = input("Enter your state: ")
                    password = input("Enter your password: ")
                    if name != None and name != "":
                        if state != None and state != "":
                            if password != None and password != "":
                                adm = Admin(name, state, password)
                                adm.add_admin()
                            else:
                                print("Please enter password")
                                continue
                        else:
                            print("Please enter your state(location)")
                            continue
                    else:
                        print("Please enter your name")
                        continue

                #Existing admin:
                elif admin_status == 2:
                    admin_id = input("Enter your admin ID: ")
                    password = input("Enter your password: ")
                    d = BoatAdmin().fetch(admin_id)
                    if d is None:
                        print("Admin id found. Try again")
                        continue
                    else:
                        if password in d:
                            pass
                        else:
                            print("Incorrect password. Try again ")
                            continue

                #Exit the program
                elif admin_status == 3:
                    print("Thank you for your visiting Panama boat services")
                    break

               

                #Table admin wants to update
                admin_top_level_options= {
                    1: "BoatInventory: Interact with Boat Inventory details",
                    2: "BoatCustomer: Interact with Boat Customer details",
                    3: "BoatKind: Interact with Boat Type details",
                    4: "BoatPrice: Interact with Boat Price details",
                    5: "BoatAdmin: Interact with Boat Admin details",
                    6: "Exit: Want to exit from program",

                }

                #Actions admin want to take on selected table
                admin_detail_level_option = {
                    1: "fetch",
                    2: "add",
                    3: "update",
                    4: "delete",
                    5: "exit"
                }

                #For top level selection
                while True:
                    format_options(admin_top_level_options)
                    top_level_option = int(input("Hi Admin, Please select the table you wish to update "))
                    if top_level_option == 6:
                        print("Thank you for visiting in Panama boat services")
                        break
                    #For any selection not from the available selections
                    if top_level_option not in admin_top_level_options:
                        print("Incorrect input received")
                        continue

                    #For detail level selection
                    while True:
                        format_options(admin_detail_level_option)
                        detail_level_option = int(input("Enter the operation you wish to perform {}: ".format(admin_top_level_options[top_level_option])))
                        if detail_level_option == 5:
                            print("Thank you for visiting in Panama boat services")
                            break

                        #For any selection not from the available selections
                        if detail_level_option not in admin_detail_level_option.keys():
                            print("Incorrect input")
                            continue

                        #Update the database accroding to selection by admin.
                        Admin().update_database(top_level_option, detail_level_option)
            break
        #For customer
        elif interacting_person == 2:
            while True:
                customer_status = int(input("Are you new or existing customer? Enter 1 for new. 2 for existing customer. 3 for exiting: "))
                #If new customer, we want to add him to database
                if customer_status == 1:
                    name = input("Enter your name: ")
                    city = input("Enter your city")
                    state = input("Enter your state(location): ")
                    ci = input("Enter your identification number( Driving license, State ID): ")
                    if name != None and name != "":
                        if city != None and city != "":
                            if state != None and state != "":
                                if ci != None and ci != "":
                                    cst = Customer(name, city, state, ci)
                                    cst.add_customer()
                

                #If existing admin, then check his customer id exist in database.
                elif customer_status == 2:
                    cust_id = input("Enter your customer ID: ")
                    data = BoatCustomer().fetch(cust_id)
                    if data is None:
                        print("Customer id found. Try again!")
                        continue
                    else:
                        pass

                elif customer_status == 3:
                    print("Thank you for visiting Panama boat services")
                    break

                #For any selection not from the available selections
                else:
                    print("Incorrect input. Try again!")
                    continue

                #Selection for customer to choose from.
                customer_options = {
                    1: "Get all available boats",
                    2: "Get all boats on my name",
                    3: "Reserve the boat",
                    4: "Cancel the boat reservation",
                    5: "Return the boat taken.",
                    6: "Exit: Want to exit from program"
                }

                while True:
                    format_options(customer_options)
                    customer_selection = int(input("Welcome customer, Please select details that you are interested in?: "))
                    if customer_selection == 6:
                        print("Thank you for visiting Panama boat services")
                        break


                    #Update the database accroding to selection by customer.
                    Customer().update_database(customer_selection)

        elif interacting_person == 3:
            print("Thank you for visiting Panama boat services")
            break



