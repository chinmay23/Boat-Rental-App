import sqlite3

'''
<><03/14/2022>
Below is the main DBBase class. Most classes are inherited from this class
'''
class DBbase:

    _conn = None
    _cursor = None

    def __init__(self, db_name = "BoatRentalsDB.sqlite"):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        raise NotImplementedError()

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

'''
<><03/14/2022>
This below class holds the inventory of the application. 
'''
class BoatInventory(DBbase):
    def __init__(self):
        super().__init__("BoatRentalsDB.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS BoatInventory;
                CREATE TABLE BoatInventory (
                    boat_model VARCHAR(10) NOT NULL PRIMARY KEY UNIQUE,
                    boat_id INTEGER,
                    is_reserved VARCHAR(3),
                    customer_id INTEGER
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, boat_model, boat_id= None, is_reserved= None, customer_id= None):
        try:
            super().connect()
            super().get_cursor.execute("""Insert into BoatInventory (boat_model, boat_id, is_reserved, customer_id) values (?,?,?,?);""", (boat_model, boat_id, is_reserved, customer_id))
            super().get_connection.commit()
            print("Boat added in inventory!")
        except Exception as e:
            print("Error: Unable to insert boat in inventory", e)
        finally:
            super().close_db()

    def delete(self, boat_model):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM BoatInventory WHERE boat_model = ?;""", (boat_model,))
            super().get_connection.commit()
            print("Boat deleted from inventory")
        except Exception as e:
            print("Error: Unable to delete boat in inventory.", e)
        finally:
            super().close_db()

    def update(self, boat_model, boat_id=None, is_reserved=None, customer_id=None):
        try:
            super().connect()
            if boat_id is not None and boat_id is not "":
                super().get_cursor.execute("""update BoatInventory set boat_id = ? WHERE boat_model = ?;""", (boat_id, boat_model,))
            if is_reserved is not None and is_reserved is not "":
                super().get_cursor.execute("""update BoatInventory set is_reserved = ? WHERE boat_model = ?;""", (is_reserved, boat_model,))
            if customer_id is not None and customer_id is not "":
                super().get_cursor.execute("""update BoatInventory set customer_id = ? WHERE boat_model = ?;""", (customer_id, boat_model,))
            super().get_connection.commit()
            print("Inventory updated")
        except Exception as e:
            print("Error: Unable to update boat in inventory. {}".format(e))
        finally:
            super().close_db()

    def fetch(self, boat_model=None):
        try:
            super().connect()
            if boat_model is not None:
                return super().get_cursor.execute("""SELECT * FROM BoatInventory WHERE boat_model = ? ;""", (boat_model,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM BoatInventory;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))
        finally:
            super().close_db()

'''
<><03/14/2022>
The below class holds the types of boats in our application. The boat types are 
small, medium and large
'''
class BoatType(DBbase):
    def __init__(self):
        super().__init__("BoatRentalsDB.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS BoatType;
                CREATE TABLE BoatType (
                    boat_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    boat_name VARCHAR(20)
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, boat_id, boat_name):
        try:
            super().connect()
            super().get_cursor.execute("""Insert into BoatType (boat_id, boat_name) values (?,?);""", (boat_id, boat_name))
            super().get_connection.commit()
            print("Added boat successfully in BoatType!")
        except Exception as e:
            print("An error occurred while inserting boat at BoatType!!.", e)
        finally:
            super().close_db()

    def update(self, boat_id, boat_name= None):
        try:
            super().connect()
            if boat_name is not None and boat_name is not "":
                super().get_cursor.execute("""update BoatType set boat_name = ? WHERE boat_id = ?;""", (boat_name, boat_id,))
                super().get_connection.commit()
                print("Updated BoatType successfully!")
        except Exception as e:
            print("An error occurred while updating BoatType : {}".format(e))
        finally:
            super().close_db()

    def delete(self, boat_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM BoatType WHERE boat_id = ?;""", (boat_id,))
            super().get_connection.commit()
            print("Boat type deleted")
        except Exception as e:
            print("Error:  Unable to delete boat type !!.", e)
        finally:
            super().close_db()

    def fetch(self, boat_id=None):
        try:
            super().connect()
            if boat_id is not None:
                return super().get_cursor.execute("""SELECT * FROM BoatType WHERE boat_model = ? ;""", (boat_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM BoatType;""").fetchall()
        except Exception as e:
            print("Error : {}".format(e))
        finally:
            super().close_db()

'''
<><03/14/2022>
This class holds the customer details in our application. The customer details are like
id, name, state and customer driving license. The primary key for this table is customer_id. 

The other methods in this class are the CRUD operations to store and retrieve 
the data from this class.
'''
class BoatCustomer(DBbase):
    def __init__(self):
        super().__init__("BoatRentalsDB.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS BoatCustomer;
                CREATE TABLE BoatCustomer (
                    customer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    customer_name VARCHAR(10),
                    customer_state VARCHAR(10),
                    customer_dl VARCHAR(15)                    
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, customer_name=None, customer_state=None, customer_dl=None):
        try:
            super().connect()
            # as customer_id is autoincrement we don't need to refer it here.
            super().get_cursor.execute("""Insert into BoatCustomer (customer_name,customer_state,customer_dl) values (?,?,?);""", (customer_name,customer_state,customer_dl))
            super().get_connection.commit()
            print("Added customer successfully in BoatCustomer!")
        except Exception as e:
            print("An error occurred while inserting customer at BoatCustomer!!.", e)
        finally:
            super().close_db()

    def update(self, customer_id, customer_name=None, customer_state=None, customer_dl=None):
        try:
            super().connect()
            if customer_name is not None and customer_name is not "":
                super().get_cursor.execute("""update BoatCustomer set customer_name = ? WHERE customer_id = ?;""", (customer_name, customer_id,))
            if customer_state is not None and customer_state is not "":
                super().get_cursor.execute("""update BoatCustomer set customer_state = ? WHERE customer_id = ?;""", (customer_state, customer_id,))
            if customer_dl is not None and customer_dl is not "":
                super().get_cursor.execute("""update BoatCustomer set customer_dl = ? WHERE customer_id = ?;""", (customer_dl, customer_id,))
            super().get_connection.commit()
            print("Updated BoatCustomer successfully!")
        except Exception as e:
            print("An error occurred while updating BoatCustomer : {}".format(e))
        finally:
            super().close_db()

    def delete(self, customer_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM BoatCustomer WHERE customer_id = ?;""", (customer_id,))
            super().get_connection.commit()
            print("Deleted customer successfully from BoatCustomer!")
        except Exception as e:
            print("An error occurred while deleting boat from BoatCustomer!!.", e)
        finally:
            super().close_db()

    def fetch(self, customer_id=None):
        try:
            super().connect()
            if customer_id is not None and customer_id is not "":
                return super().get_cursor.execute("""SELECT * FROM BoatCustomer WHERE customer_id = ? ;""", (customer_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM BoatCustomer;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))
        finally:
            super().close_db()

'''
<><03/14/2022>
This class holds the prices of different types of boats per day that we have in our application. 
The primary key for this table is boat_id. 

The other methods in this class are the CRUD operations to store and retrieve 
the data from this class.
'''
class BoatPrice(DBbase):
    def __init__(self):
        super().__init__("BoatRentalsDB.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS BoatPrice;
                CREATE TABLE BoatPrice (
                    boat_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    boat_price INTEGER
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, boat_id, boat_price):
        try:
            super().connect()
            super().get_cursor.execute("""Insert into BoatPrice (boat_id, boat_price) values (?,?);""", (boat_id, boat_price))
            super().get_connection.commit()
            super().close_db()
            print("Added boat successfully in BoatPrice!")
        except Exception as e:
            print("An error occurred while inserting boat at BoatPrice!!.", e)
        finally:
            super().close_db()

    def update(self, boat_id, boat_price=None):
        try:
            super().connect()
            if boat_price is not None and boat_price is not "":
                super().get_cursor.execute("""update BoatPrice set boat_price = ? WHERE boat_id = ?;""", (boat_price, boat_id,))
                super().get_connection.commit()
                print("Updated BoatPrice successfully!")
        except Exception as e:
            print("An error occurred while updating BoatPrice : {}".format(e))
        finally:
            super().close_db()

    def delete(self, boat_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM BoatPrice WHERE boat_id = ?;""", (boat_id,))
            super().get_connection.commit()
            print("Deleted price successfully from BoatPrice!")
        except Exception as e:
            print("An error occurred while deleting boat from BoatPrice!!.", e)
        finally:
            super().close_db()

    def fetch(self, boat_id=None):
        try:
            super().connect()
            if boat_id is not None:
                return super().get_cursor.execute("""SELECT * FROM BoatPrice WHERE boat_id = ? ;""", (boat_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM BoatPrice;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))
        finally:
            super().close_db()

'''
<><03/14/2022>
This class holds the Admin details of our application. 
The primary key for this table is admin_id. 

The other methods in this class are the CRUD operations to store and retrieve 
the data from this class.
'''
class BoatAdmin(DBbase):
    def __init__(self):
        super().__init__("BoatRentalsDB.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS BoatAdmin;
                CREATE TABLE BoatAdmin (
                    admin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    admin_name VARCHAR(10),
                    admin_state VARCHAR(10),
                    admin_password VARCHAR(15)
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, admin_name=None, admin_state=None, admin_password=None):
        try:
            super().connect()
            # as admin_id is autoincrement we don't need to refer it here.
            super().get_cursor.execute("""Insert into BoatAdmin (admin_name,admin_state,admin_password) values (?,?,?);""", (admin_name,admin_state,admin_password))
            super().get_connection.commit()
            print("Added admin successfully in BoatAdmin!")
        except Exception as e:
            print("An error occurred while inserting admin at BoatAdmin!!.", e)
        finally:
            super().close_db()

    def update(self, admin_id, admin_name=None, admin_state=None, admin_password=None):
        try:
            super().connect()
            if admin_name is not None and admin_name is not "":
                super().get_cursor.execute("""update BoatAdmin set admin_name = ? WHERE admin_id = ?;""", (admin_name, admin_id,))
            if admin_state is not None and admin_state is not "":
                super().get_cursor.execute("""update BoatAdmin set admin_state = ? WHERE admin_id = ?;""", (admin_state, admin_id,))
            if admin_password is not None and admin_password is not "":
                super().get_cursor.execute("""update BoatAdmin set admin_password = ? WHERE admin_id = ?;""", (admin_password, admin_id,))
            super().get_connection.commit()
            print("Updated BoatAdmin successfully!")
        except Exception as e:
            print("An error occurred while updating BoatAdmin : {}".format(e))
        finally:
            super().close_db()

    def delete(self, admin_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM BoatAdmin WHERE admin_id = ?;""", (admin_id,))
            super().get_connection.commit()
            print("Deleted admin successfully from BoatAdmin!")
        except Exception as e:
            print("An error occurred while deleting admin from BoatAdmin!!.", e)
        finally:
            super().close_db()

    def fetch(self, admin_id=None):
        try:
            super().connect()
            if admin_id is not None:
                return super().get_cursor.execute("""SELECT * FROM BoatAdmin WHERE admin_id = ? ;""", (admin_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM BoatAdmin;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))
        finally:
            super().close_db()

if __name__ == '__main__':
    pass
   







