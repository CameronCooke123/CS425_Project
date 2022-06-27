import psycopg2
#import psycopg2.extras

hostname = 'localhost'
database = 'CS 425 Project'
username = 'postgres'
pwd = 'password'
port_id = 5433
conn = None
cur = None

def main ():
    try:
        with psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        ) as conn:
            with conn.cursor() as cur:
            #with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(create_tables_code)
                conn.commit()
                sql_string = None
                #get input loop
                while True:
                    select_command = input(
"""Available Commands: 
     1: Create/Modify Product
     2: Delete Product
     3: Create New Warehouse
     4: Add Stock to Warehouse
     5: View Items in Warehouse by Name
     6: View Items in Warehouse by Type
     7: Add/Modify Product Price
     8: Delete Product Price
     9: Add/Modify Customer Address
    10: Delete Customer Address
    11: Add/Modify Customer Credit Card
    12: Delete Customer Credit Card
    e: Exit
Please Enter a Command: """)
                    if select_command == "1":
                        sql_string = CreateModifyProduct()
                    elif select_command == "2":
                        sql_string = DeleteProduct()
                    elif select_command == "3":
                        sql_string = CreateWarehouse()
                    elif select_command == "4":
                        sql_string = AddStock()
                    elif select_command == "5":
                        sql_string = ViewProductsInWarehouse("name")
                    elif select_command == "6":
                        sql_string = ViewProductsInWarehouse("type")
                    elif select_command == "7":
                        sql_string = AddModifyPrice()
                    elif select_command == "8":
                        sql_string = DeletePrice()
                    elif select_command == "9":
                        sql_string = AddModifyCustAddr()
                    elif select_command == "10":
                        sql_string = DeleteCustAddr()
                    elif select_command == "11":
                        sql_string = AddModifyCC()
                    elif select_command == "12":
                        sql_string = DeleteCC()
                    else:
                        break

                    cur.execute(sql_string)
                    conn.commit()

                    if select_command == "5" or select_command == "6":
                        print(f"{'Product ID':20}{'Warehouse ID':20}{'Number In Stock':20}{'Product Name':20}{'Product Category':20}{'Product Type':20}{'Product Size':20}")
                        for result in cur.fetchall():
                            print(f"{str(result[0]):20}{str(result[1]):20}{str(result[2]):20}{str(result[3]):20}{str(result[4]):20}{str(result[5]):20}{str(result[6]):20}")

                    print("\nCommand executed successfully\n")

    except Exception as error:
        print("\n")
        print(error)
        print("\n")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def CreateModifyProduct ():
    pid = input("Enter product ID: ")
    name = input("Enter product name: ")
    category = input("Enter product category: ")
    prod_type = input("Enter product type: ")
    size = input("Enter product size: ")

    return "INSERT INTO product " \
           "VALUES ('%s', '%s', '%s', '%s', '%s') " \
           "ON CONFLICT (pid) DO UPDATE " \
           "SET name = '%s', category = '%s', type = '%s', size = '%s';" \
           % (pid, name, category, prod_type, size, name, category, prod_type, size)

def DeleteProduct ():
    pid = input("Enter product ID: ")
    return "DELETE FROM product " \
           "WHERE pid = '%s'" \
           % (pid)

def CreateWarehouse ():
    whid = input("Enter warehouse ID: ")
    stAdd = input("Enter the street address: ")
    city = input("Enter the city: ")
    state = input("Enter the state: ")
    zipCode = input("Enter the zip code: ")
    capacity = input("Enter the warehouse capacity: ")

    return "INSERT INTO warehouse VALUES (" + whid + ", " + capacity + ", '" + stAdd + "', '" + city + "', '" + state +\
           "', '" + zipCode + "');"

def AddStock ():
    whid = input("Enter warehouse ID: ")
    pid = input("Enter the product ID: ")
    count = input("Enter the number of the product being added: ")

    return "INSERT INTO wh_stock VALUES (" + whid + ", " + pid + ", " + count + ");"

def ViewProductsInWarehouse (byWhat):
    whid = input("Enter the warehouse id (can be 'all'): ")
    name_or_type = input("Enter the product " + byWhat + " (can be 'all'): ")
    sql_string = "SELECT * FROM wh_stock JOIN product USING (pid) "

    if whid != 'all':
        sql_string += "WHERE whid = " + whid
        if name_or_type != 'all':
            sql_string += " AND " + byWhat + " = '" + name_or_type + "'"
    elif name_or_type != 'all':
        sql_string += "WHERE " + byWhat + " = '" + name_or_type + "'"
    sql_string += ";"

    return sql_string

def AddModifyPrice ():
    pid = input("Enter product ID: ")
    state = input("Enter the state: ")
    price = input("Enter the dollar amount: ")
    return "INSERT INTO prod_price " \
           "VALUES ('%s', '%s', '%s') " \
           "ON CONFLICT (pid, state) DO UPDATE " \
           "SET state = '%s', dollaramt = '%s';" \
           % (pid, state, price, state, price)

def DeletePrice ():
    pid = input("Enter product ID: ")
    state = input("Enter the state: ")
    return "DELETE FROM prod_price " \
           "WHERE pid = '%s' and state = '%s'" \
           % (pid, state)

def AddModifyCustAddr ():
    cid = input("Enter the customer ID: ")
    st_addr = input("Enter the street address: ")
    city = input("Enter the city: ")
    state = input("Enter the state: ")
    zip_code = input("Enter the zip code: ")
    return "INSERT INTO cust_addr " \
           "VALUES ('%s', '%s', '%s', '%s', '%s') " \
           "ON CONFLICT (cid) DO UPDATE " \
           "SET staddr = '%s', city = '%s', state = '%s', zipcode = '%s';" \
           % (cid, st_addr, city, state, zip_code, st_addr, city, state, zip_code)

def DeleteCustAddr ():
    cid = input("Enter the customer ID: ")
    st_addr = input("Enter the street address: ")
    city = input("Enter the city: ")
    state = input("Enter the state: ")
    zip_code = input("Enter the zip code: ")
    return "DELETE FROM cust_addr " \
           "WHERE cid = '%s' " \
           "AND staddr = '%s' " \
           "AND city = '%s' " \
           "AND state = '%s' " \
           "AND zipcode = '%s';" \
           % (cid, st_addr, city, state, zip_code)

def AddModifyCC ():
    cid = input("Enter customer ID: ")
    ccNum = input("Enter credit card number: ")
    secCode = input("Enter security code: ")
    exp = input("Enter expiration date: ")
    name = input("Enter the name on card: ")
    line1 = "INSERT INTO creditcard " \
            "VALUES ('%s', '%s', '%s', '%s') " \
            "ON CONFLICT (mainNumber) DO UPDATE " \
            "SET seccode = '%s', expirydate = '%s', nameoncard = '%s';" \
            % (ccNum, secCode, exp, name, secCode, exp, name)
    return line1 + "INSERT INTO cust_cc " \
                   "VALUES ('%s', '%s') " \
                   "ON CONFLICT (mainnumber) DO UPDATE " \
                   "SET cid = '%s';" \
                   % (ccNum, cid, cid)

def DeleteCC ():
    ccNum = input("Enter the credit card number: ")
    line1 = "DELETE FROM cust_cc " \
            "WHERE mainnumber = '%s';" \
            % (ccNum)
    return line1 + "DELETE FROM creditcard " \
                   "WHERE mainnumber = '%s';" \
                   % (ccNum)

create_tables_code = '''
        CREATE TABLE IF NOT EXISTS Customer (
          cid int, 
          firstName varchar,
          lastName varchar,
          balance int,
          PRIMARY KEY (cid)
        );
        --DROP TABLE Address;
        CREATE TABLE IF NOT EXISTS Address (
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (stAddr, city, state, zipCode)
        );
        CREATE TABLE IF NOT EXISTS StaffMember (
          sid int,
          firstName varchar,
          lastName varchar,
          salary int CHECK (salary > 0),
          jobTitle varchar,
          PRIMARY KEY (sid)
        );
        CREATE TABLE IF NOT EXISTS CreditCard (
          mainNumber numeric(16),
          secCode numeric(3),
          expiryDate numeric(4),
          nameOnCard varchar,
          PRIMARY KEY (mainNumber)
        );
        --DROP TYPE IF EXISTS delStatus CASCADE;
        --CREATE TYPE delStatus AS ENUM ('issued', 'sent', 'received');
        CREATE TABLE IF NOT EXISTS CustOrder (
          orderID int,
          dateIssued numeric(8), --mmddyyyy
          status delStatus,
          PRIMARY KEY (orderID)
        );
        /*ALTER TABLE warehouse
            ADD COLUMN stAddr varchar,
            ADD COLUMN city varchar,
            ADD COLUMN state char(2),
            ADD COLUMN zipCode varchar;*/
        --DELETE FROM warehouse;
        CREATE TABLE IF NOT EXISTS Warehouse (
          whid int,
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          capacity int CHECK (capacity >= 0),
          PRIMARY KEY (whid)
        );
        CREATE TABLE IF NOT EXISTS Supplier (
          name varchar,
          PRIMARY KEY (name)
        );
        CREATE TABLE IF NOT EXISTS Product (
          pid numeric,
          name varchar,
          category varchar,
          type varchar,
          size real CHECK (size > 0),
          PRIMARY KEY (pid)
        );
        --create relation tables
        CREATE TABLE IF NOT EXISTS Cust_Addr (
          cid integer,
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (cid)
          --FOREIGN KEY (cid) references Customer,
          --FOREIGN KEY (stAddr, city, state, zipCode) references Address
        );
        CREATE TABLE IF NOT EXISTS Cust_CC (
          mainNumber numeric(16),
          cid int,
          PRIMARY KEY (mainNumber),
          FOREIGN KEY (mainNumber) references CreditCard
          --FOREIGN KEY (cid) references Customer
        );
        CREATE TABLE IF NOT EXISTS CC_Billing_Addr (
          mainNumber numeric(16),
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (mainNumber),
          FOREIGN KEY (mainNumber) references CreditCard,
          FOREIGN KEY (stAddr, city, state, zipCode) references Address
        );
        CREATE TABLE IF NOT EXISTS Ordered_By (
          orderID int,
          cid int,
          PRIMARY KEY (orderID),
          FOREIGN KEY (orderID) references CustOrder,
          FOREIGN KEY (cid) references Customer
        );
        CREATE TABLE IF NOT EXISTS Order_Paid_With (
          orderID int,
          mainNumber numeric(16),
          PRIMARY KEY (orderID),
          FOREIGN KEY (orderID) references CustOrder,
          FOREIGN KEY (mainNumber) references CreditCard
        );
        CREATE TABLE IF NOT EXISTS Staff_Addr (
          sid int,
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (sid),
          FOREIGN KEY (sid) references StaffMember,
          FOREIGN KEY (stAddr, city, state, zipCode) references Address
        );
        --DROP TABLE WH_Addr;
        /*CREATE TABLE IF NOT EXISTS WH_Addr (
          whid int,
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (whid),
          FOREIGN KEY (whid) references Warehouse
        );*/
        CREATE TABLE IF NOT EXISTS Supp_Addr (
          name varchar,
          stAddr varchar,
          city varchar,
          state char(2),
          zipCode varchar,
          PRIMARY KEY (name),
          FOREIGN KEY (name) references Supplier,
          FOREIGN KEY (stAddr, city, state, zipCode) references Address
        );
        CREATE TABLE IF NOT EXISTS WH_Stock (
          whid int,
          pid int,
          numberInStock int CHECK (numberInStock > 0),
          PRIMARY KEY (whid, pid),
          FOREIGN KEY (whid) references Warehouse,
          FOREIGN KEY (pid) references Product
        );
        CREATE TABLE IF NOT EXISTS Supp_Prod (
          name varchar,
          pid int,
          supplierPrice int CHECK (supplierPrice > 0),
          PRIMARY KEY (name, pid),
          FOREIGN KEY (name) references Supplier,
          FOREIGN KEY (pid) references Product
        );
        --DROP TABLE Prod_Price;
        CREATE TABLE IF NOT EXISTS Prod_Price (
          pid int,
          state char(2),
          dollarAmt real CHECK (dollarAmt > 0),
          PRIMARY KEY (pid, state),
          FOREIGN KEY (pid) references Product
        );
        CREATE TABLE IF NOT EXISTS Prod_In_Order (
          orderID int,
          pid int,
          numberOfProduct int CHECK (numberOfProduct > 0),
          PRIMARY KEY (orderID, pid),
          FOREIGN KEY (orderID) references CustOrder,
          FOREIGN KEY (pid) references Product
        );
        CREATE TABLE IF NOT EXISTS Alcohol (
          pid int,
          alcContent real CHECK (alcContent <= 1 AND alcContent >= 0),
          PRIMARY KEY (pid),
          FOREIGN KEY (pid) references Product
        );
        CREATE TABLE IF NOT EXISTS Food (
          pid int,
          calories int CHECK (calories > 0),
          carbs int CHECK (carbs > 0),
          fat int CHECK (fat > 0),
          protein int CHECK (protein > 0),
          sodium int CHECK (sodium > 0),
          PRIMARY KEY (pid),
          FOREIGN KEY (pid) references Product
        );'''

if __name__ == '__main__':
    main()

