# A2 COMP348 by Ralph Elhage, ID: 40131981
# server and client hosted on same netork, same device, following IPV4 (local) addresses instead of public ip adresses
import socket

# max bytes of header msg, which contains the amount of bytes in next msg to be received by server
HEADER = 99
# gets ipv4 address (private address), can also be found through from cmdline -> ipconfig
IPADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 9999
FORMAT = 'utf-8'

# list of records, each record to be in tuple format
records = []

# ipv4 family, stream type TCP
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds socket to ipv4 address & port the server is running off of
sock_server.bind((IPADDRESS, PORT))


# generates DB as a list of tuples, formatted & without duplicates
def generateDB(records):
    file = open("data.txt", "r")  # open in read mode

    while True:
        # return next line from file
        line = file.readline()
        # When empty line reached, stop reading
        if not line:
            break
        # split() converts line str to list of elements that were separated by '|'
        line_list = line.split('|')
        # removes extra whitespace
        for index, element in enumerate(line_list):
            line_list[index] = element.strip()
        # tuple() converts list to tuple
        line_tuple = tuple(line_list)
        # stores tuples in list if name isnt empty
        if not(line_tuple[0] == ''):
            if (len(records) == 0):
                records.append(line_tuple)
            else:
                # ensures name is unique before adding tuple to list
                for iteration, record in enumerate(records):
                    if line_tuple[0] == record[0]:
                        # duplicate found, skip over it
                        break
                    elif iteration == len(records)-1:
                        records.append(line_tuple)
    file.close()


def start():
    print("- SERVER STARTING -")
    sock_server.listen()
    print(f"- SERVER LISTNENING ON {IPADDRESS}, OFF PORT #{PORT} -")

    while True:
        # awaits connection to server
        # "conn" is new socket object usable to send and receive data on the connection
        # "address" is the address bound to the socket on the other end of the connection
        (conn, addr) = sock_server.accept()
        # No threading needed to manage clients since a max of 1 client can be connected simultaneously
        print("- CONNECTION CONFIRMED -")

        # Option selected from the print menu registered as selection
        selection = receive(conn)

        if selection == "1":
            print("Find Customer requested by client ...")
            findCustomer(conn, records)

        elif selection == "2":
            print("Add Customer requested by client ...")
            addCustomer(conn, records)
            sendReport(conn, records)

        elif selection == "3":
            print("Delete Customer requested by client ...")
            deleteCustomer(conn, records)
            sendReport(conn, records)

        elif selection == "4":
            print("Update Age requested by client ...")
            updateAge(conn, records)
            sendReport(conn, records)

        elif selection == "5":
            print("Update Address requested by client ...")
            updateAddress(conn, records)
            sendReport(conn, records)

        elif selection == "6":
            print("Update Phone Number requested by client ...")
            updatePhone(conn, records)
            sendReport(conn, records)

        elif selection == "7":
            print("Print Report requested by client ...")
            sendReport(conn, records)

        conn.close()


# sends a str to client
def send(conn, msg):
    msg_formatted = msg.encode(FORMAT)
    msgLength_formatted = str(len(msg_formatted)).encode(FORMAT)
    # next line adds whitespace (formatted) to fill header size
    msgLength_formatted += b' ' * (HEADER - len(msgLength_formatted))
    conn.send(msgLength_formatted)
    conn.send(msg_formatted)


# receives a str from client
def receive(conn):
    # awaits to receive header msg from client, then decodes it from byte format to string
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:  # in order to parse, making sure msg_length isnt blank
        msg_length = int(msg_length)
        # awaits to receive msg (of nb of bytes in header msg) from client
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg


# sends report to client
def sendReport(conn, records):
    send(conn, "** Python DB contents **")
    for record in records:
        send(conn, '|'.join(record))


# receives customer name from client, sends customer to client
def findCustomer(conn, records):
    nameSearched = receive(conn)
    for iteration, record in enumerate(records):
        if record[0] == nameSearched:
            send(conn, "Server response: "+('|'.join(record)))
            return
        elif iteration == len(records)-1:
            send(conn, "Server response: "+nameSearched+" not found in database")


# receives customer name; if unique, receives customer characteristics and adds customer to db
def addCustomer(conn, records):
    name = receive(conn)
    for record in records:
        if record[0] == name:
            send(conn, "Server response: Customer already exists")
            return
    send(conn, "")  # client expects to receive in case customer already exists
    age = receive(conn)
    address = receive(conn)
    phone = receive(conn)
    records.append((name, age, address, phone))


def deleteCustomer(conn, records):
    name = receive(conn)
    for iteration, record in enumerate(records):
        if record[0] == name:
            records.remove(record)
            send(conn, "Server response: Customer removed successfully")
            return
        elif (iteration == len(records)-1):
            send(conn, "Server response: Customer does not exist")


def updateAge(conn, records):
    name = receive(conn)
    for iteration, record in enumerate(records):
        if record[0] == name:
            send(conn, "")
            age = receive(conn)
            record = list(record)
            record[1] = age
            records[iteration] = tuple(record)
            return
        elif iteration == len(records)-1:
            send(conn, "Server response: "+name+" not found in database")


def updateAddress(conn, records):
    name = receive(conn)
    for iteration, record in enumerate(records):
        if record[0] == name:
            send(conn, "")
            address = receive(conn)
            record = list(record)
            record[2] = address
            records[iteration] = tuple(record)
            return
        elif iteration == len(records)-1:
            send(conn, "Server response: "+name+" not found in database")


def updatePhone(conn, records):
    name = receive(conn)
    for iteration, record in enumerate(records):
        if record[0] == name:
            send(conn, "")
            phone = receive(conn)
            record = list(record)
            record[3] = phone
            records[iteration] = tuple(record)
            return
        elif iteration == len(records)-1:
            send(conn, "Server response: "+name+" not found in database")


generateDB(records)
start()
