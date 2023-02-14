# A2 COMP348 by Ralph Elhage, ID: 40131981
import socket
import sys

# max bytes of header msg, which contains the amount of bytes in next msg to be received by server
HEADER = 99
# gets ipv4 address (private address), can also be found through from cmdline -> ipconfig
IPADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 9999
FORMAT = 'utf-8'

# ipv4 family, stream type TCP
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds socket to ipv4 address & port the server is running off of
sock_client.connect((IPADDRESS, PORT))


# sending a str to server
def send(msg):
    msg_formatted = msg.encode(FORMAT)
    msgLength_formatted = str(len(msg_formatted)).encode(FORMAT)
    # next line adds whitespace (formatted) to fill header size
    msgLength_formatted += b' ' * (HEADER - len(msgLength_formatted))
    sock_client.send(msgLength_formatted)
    sock_client.send(msg_formatted)


# receive a str from server and prints it
def receive():
    # awaits to receive header msg from client, then decodes it from byte format to string
    msg_length = sock_client.recv(HEADER).decode(FORMAT)
    if msg_length:  # in order to parse, making sure msg_length isnt blank
        msg_length = int(msg_length)
        # awaits to receive msg (of nb of bytes in header msg) from client
        msg = sock_client.recv(msg_length).decode(FORMAT)
        print(msg)
        return msg


# prints the report received from server
def receiveReport():
    print()
    while not(receive() == None):
        receive()
    print()


# sends customer name to server, receives customer from server
def findCustomer():
    print("\n========= FIND CUSTOMER =========")
    nameSearched = input("Customer Name: ")
    send(nameSearched)
    receive()


def addCustomer():
    print("\n========= ADD CUSTOMER =========")
    name = input("Enter new customer's name: ")
    send(name)
    checkValid = receive()
    # if unique, proceed
    if checkValid == "":
        age = input("Enter new customer's age: ")
        address = input("Enter new customer's address: ")
        phone = input("Enter new customer's phone number: ")
        send(age)
        send(address)
        send(phone)
    else:
        return


def deleteCustomer():
    print("\n========= DELETE CUSTOMER =========")
    name = input("Enter the name of the customer you want to delete: ")
    send(name)
    receive()  # successful or not


def updateAge():
    print("\n========= UPDATE CUSTOMER AGE =========")
    name = input(
        "Enter the name of the customer whose age you want to update: ")
    send(name)
    checkValid = receive()
    # if unique, proceed
    if checkValid == "":
        age = input("Enter customer's updated age: ")
        send(age)
    else:
        return


def updateAddress():
    print("\n========= UPDATE CUSTOMER ADDRESS =========")
    name = input(
        "Enter the name of the customer whose address you want to update: ")
    send(name)
    checkValid = receive()
    # if unique, proceed
    if checkValid == "":
        address = input("Enter customer's updated address: ")
        send(address)
    else:
        return


def updatePhone():
    print("\n========= UPDATE CUSTOMER PHONE NUMBER =========")
    name = input(
        "Enter the name of the customer whose phone number you want to update: ")
    send(name)
    checkValid = receive()
    # if unique, proceed
    if checkValid == "":
        phone = input("Enter customer's updated phone number: ")
        send(phone)
    else:
        return


def menuSelection():
    print('''
    Python DB Menu
    1. Find customer
    2. Add customer
    3. Delete customer
    4. Update customer age
    5. Update customer address
    6. Update customer phone
    7. Print report
    8. Exit
    ''')
    selection = input("Select: ")
    # input verification
    while (not(selection.isnumeric()) or not(len(selection) == 1)) or (int(selection) < 1 or int(selection) > 8):
        selection = input("Invalid option. Select (1 to 8): ")

    if selection == "8":
        print("Terminating Client ...")
        print('''
        ----------------------
                GOODBYE
        ----------------------''')
        sys.exit(0)
    else:
        send(selection)

    if selection == "1":
        findCustomer()

    elif selection == "2":
        addCustomer()
        receiveReport()

    elif selection == "3":
        deleteCustomer()
        receiveReport()

    elif selection == "4":
        updateAge()
        receiveReport()

    elif selection == "5":
        updateAddress()
        receiveReport()

    elif selection == "6":
        updatePhone()
        receiveReport()

    elif selection == "7":
        receiveReport()


while True:
    print("--------------------------------------")
    menuSelection()
    sock_client.shutdown(socket.SHUT_RDWR)
    sock_client.close()
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_client.connect((IPADDRESS, PORT))
    print()
