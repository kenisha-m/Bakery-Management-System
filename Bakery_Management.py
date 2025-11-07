import mysql.connector as sqlter

mycon= sqlter.connect(host="localhost", user="root", passwd="unlock", ssl_disabled=True)
c= mycon.cursor()

c.execute("CREATE DATABASE IF NOT EXISTS bakery")
c.execute("USE bakery")

c.execute("CREATE TABLE IF NOT EXISTS Items (i_id INT PRIMARY KEY, i_name VARCHAR(30),i_qty INT, i_price INT)")

c.execute("CREATE TABLE IF NOT EXISTS Workers (w_id INT PRIMARY KEY, w_name VARCHAR(20), w_salary INT, w_designation VARCHAR(25))")

c.execute("CREATE TABLE IF NOT EXISTS Sales (bill_no INT PRIMARY KEY, amount INT, c_name VARCHAR(20), phone_no BIGINT)")
mycon.commit()

a= """INSERT INTO Items (i_id, i_name, i_qty, i_price) VALUES
(14, 'Chocolate Pastry', 20, 350),
(18, 'Apple Pie', 30, 300),
(19, 'Banana Muffins', 15, 200),
(29, 'Chocolate Cookies', 40, 100)
"""
c.execute(a)
mycon.commit()

b= """INSERT INTO Workers (w_id, w_name, w_salary, w_designation) VALUES
(25, 'Lisa', 55000, 'Head Baker'),
(26, 'Alex', 35000, 'Pastry Chef'),
(27, 'Peter', 25000, 'Assistant Baker'),
(28, 'Sam', 20000, 'Cashier')
"""
c.execute(b)
mycon.commit()

d= """INSERT INTO Sales (bill_no, amount, c_name, phone_no) VALUES
(1, 600, 'Bob', 9204576361),
(2, 1000, 'Alya', 6745839563),
(3, 1400, 'Jacob', 9384563472),
(4, 900, 'Tom', 8374626573)
"""
c.execute(d)
mycon.commit()


# ----------------- ITEMS -----------------

def insertitem():
    i_id = int(input("Enter item id: "))
    iname = input("Enter item name: ")
    iqty = int(input("Enter quantity: "))
    iprice = int(input("Enter price: "))
    st = "INSERT INTO Items VALUES({}, '{}', {}, {})".format(i_id, iname, iqty, iprice)
    c.execute(st)
    mycon.commit()
    print("Item inserted successfully.\n")

def updateitem():
    print("1. Update stock")
    print("2. Update price")
    ch = int(input("Enter choice: "))
    if ch == 1:
        icode = int(input("Enter item ID to update: "))
        c.execute("SELECT * FROM Items WHERE i_id={}".format(icode))
        if c.fetchone():
            cqty = int(input("Enter new quantity: "))
            c.execute("UPDATE Items SET i_qty={} WHERE i_id={}".format(cqty, icode))
            mycon.commit()
            print("Stock updated successfully.\n")
        else:
            print("Invalid item ID.\n")
    elif ch == 2:
        icode = int(input("Enter item ID to update: "))
        c.execute("SELECT * FROM Items WHERE i_id={}".format(icode))
        if c.fetchone():
            price = int(input("Enter new price: "))
            c.execute("UPDATE Items SET i_price={} WHERE i_id={}".format(price, icode))
            mycon.commit()
            print("Price updated successfully.\n")
        else:
            print("Invalid item ID.\n")
    else:
        print("Invalid choice.\n")

def deleteitem():
    icode = int(input("Enter item ID to delete: "))
    c.execute("DELETE FROM Items WHERE i_id={}".format(icode))
    mycon.commit()
    print("Item deleted successfully.\n")

def displayitems():
    c.execute("SELECT * FROM Items")
    data = c.fetchall()
    print("Item ID\tName\t\tQty\tPrice")
    for i in data:
        print(i[0], "\t", i[1], "\t\t", i[2], "\t", i[3])
    print()

# ----------------- WORKERS -----------------

def insertworker():
    wid = int(input("Enter worker ID: "))
    wname = input("Enter name: ")
    wsalary = int(input("Enter salary: "))
    wdesig = input("Enter designation: ")
    st = "INSERT INTO Workers VALUES({}, '{}', {}, '{}')".format(wid, wname, wsalary, wdesig)
    c.execute(st)
    mycon.commit()
    print("Worker added successfully.\n")

def updateworker():
    print("1. Update salary")
    print("2. Update designation")
    ch = int(input("Enter choice: "))
    wcode = int(input("Enter worker ID: "))
    c.execute("SELECT * FROM Workers WHERE w_id={}".format(wcode))
    if c.fetchone():
        if ch == 1:
            new_salary = int(input("Enter new salary: "))
            c.execute("UPDATE Workers SET w_salary={} WHERE w_id={}".format(new_salary, wcode))
            mycon.commit()
            print("Salary updated successfully.\n")
        elif ch == 2:
            new_desig = input("Enter new designation: ")
            c.execute("UPDATE Workers SET w_designation='{}' WHERE w_id={}".format(new_desig, wcode))
            mycon.commit()
            print("Designation updated successfully.\n")
        else:
            print("Invalid choice.\n")
    else:
        print("Invalid worker ID.\n")

def deleteworker():
    wid = int(input("Enter worker ID to delete: "))
    c.execute("DELETE FROM Workers WHERE w_id={}".format(wid))
    mycon.commit()
    print("Worker deleted successfully.\n")

def displayworkers():
    c.execute("SELECT * FROM Workers")
    data = c.fetchall()
    print("ID\tName\t\tSalary\tDesignation")
    for i in data:
        print(i[0], "\t", i[1], "\t\t", i[2], "\t", i[3])
    print()

# ----------------- SALES -----------------

def placeorder():
    cname = input("Enter customer name: ")
    cphone = int(input("Enter customer phone number: "))

    c.execute("SELECT * FROM Items")
    items = c.fetchall()

    order_list = []
    total = 0
    ch = "y"

    while ch.lower() == "y":
        item_id = int(input("Enter item ID: "))
        qty = int(input("Enter quantity: "))
        for item in items:
            if item[0] == item_id:
                total += item[3] * qty
                order_list.append((item[1], qty, item[3]))
                break
        else:
            print("Invalid item ID.")
        ch = input("Add more items? (y/n): ")

    c.execute("SELECT * FROM Sales")
    s = c.fetchall()
    bill_no = 100 + len(s)

    print("\n----- BILL -----")
    print("Bill No.:", bill_no)
    print("Customer:", cname)
    print("Phone:", cphone)
    print("\nItem\tQty\tPrice\tTotal")
    for o in order_list:
        print(f"{o[0]}\t{o[1]}\t{o[2]}\t{o[1]*o[2]}")
    print("------------------")
    print("Total Bill Amount:", total)
    print("------------------\n")

    c.execute("INSERT INTO Sales VALUES({}, {}, '{}', {})".format(bill_no, total, cname, cphone))
    mycon.commit()
    print("Order placed successfully!\n")

def displaysales():
    c.execute("SELECT * FROM Sales")
    data = c.fetchall()
    print("Bill No.\tAmount\tCustomer Name\tPhone No.")
    for i in data:
        print(i[0], "\t", i[1], "\t", i[2], "\t", i[3])
    print()

def bakeryrevenue():
    c.execute("SELECT SUM(amount) FROM Sales")
    r = c.fetchone()[0]
    print("\nTotal Bakery Revenue:", r if r else 0, "\n")

# ----------------- MAIN MENU -----------------

print("WELCOME TO THE BAKEHOUSE")

while True:
    print("""
MAIN MENU:
1. WORKERS
2. ITEMS
3. SALES
4. EXIT
""")
    ch = int(input("Enter your choice: "))

    if ch == 1:
        while True:
            print("""
WORKERS MENU:
1. Add Worker
2. Delete Worker
3. Update Worker
4. View Workers
5. Back
""")
            c1 = int(input("Enter your choice: "))
            if c1 == 1:
                insertworker()
            elif c1 == 2:
                deleteworker()
            elif c1 == 3:
                updateworker()
            elif c1 == 4:
                displayworkers()
            elif c1 == 5:
                break
            else:
                print("Invalid choice.\n")

    elif ch == 2:
        while True:
            print("""
ITEMS MENU:
1. Add Item
2. Delete Item
3. Update Item
4. View Items
5. Back
""")
            c2 = int(input("Enter your choice: "))
            if c2 == 1:
                insertitem()
            elif c2 == 2:
                deleteitem()
            elif c2 == 3:
                updateitem()
            elif c2 == 4:
                displayitems()
            elif c2 == 5:
                break
            else:
                print("Invalid choice.\n")

    elif ch == 3:
        while True:
            print("""
SALES MENU:
1. Place Order
2. View Sales
3. View Bakery Revenue
4. Back
""")
            c3 = int(input("Enter your choice: "))
            if c3 == 1:
                placeorder()
            elif c3 == 2:
                displaysales()
            elif c3 == 3:
                bakeryrevenue()
            elif c3 == 4:
                break
            else:
                print("Invalid choice.\n")

    elif ch == 4:
        print("Thank you for visiting The Bakehouse!")
        break

    else:
        print("Invalid choice.\n")