import os
import time
import serial
import serial.tools.list_ports

############### SETUP COM PORT ###############
def com_check():
    good_port = False
    ports = serial.tools.list_ports.comports()
    for portlist, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(portlist, desc, hwid))
    while not(good_port):
        port_selection = input("Enter COM port number for data transfer : ")
        try:
            port_number = int(port_selection)
        except:
            print("Please enter only the number of the COM port to use, try again.")
            continue
        port_selection = "COM"+str(port_number)
        print(port_selection)
        if port_selection not in portlist:
            print("Not a valid COM port option, try again.")
        else:
            good_port = True
            return port_selection

############### FILE SELECTION ###############
def file_selection(): 
    file_confirmed = False 
    while not(file_confirmed):
        print("Current filepath is "+os.path.abspath(__file__))
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        files_at_path = os.listdir(os.curdir)
        print("Local files are: ")
        for x in range(len(files_at_path)):
            print(files_at_path[x])
        user_input = input("Enter filename that you would like to transfer OR (n)o to change directories: ")
        if user_input.lower() == 'no' or user_input.lower() == 'n':
            print("user requested changing directories")
            # change directory TODO
            continue
        elif user_input not in files_at_path:
            print("File does not exist as typed, try again.")
            continue
        else:
            file_to_transfer = user_input
            file_confirmed = True
            return file_to_transfer
        


############### TRANSFER ###############
#count = 0

#while 1:
#    ser.write('Sent %d time(s)')
#    time.sleep(1)
#    count += 1

file_to_transfer = file_selection()
f = open(file_to_transfer, "r")
print(f.read()) 

############### MAIN ###############
ser = serial.Serial(com_check(), 9600, timeout=0.050)       # hard-coding to 9600 baud since that's what MS-SID uses, expand this later if used for other projects
transfer()
time.sleep(1)
receive()