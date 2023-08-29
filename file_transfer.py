import os
import time
import serial
import serial.tools.list_ports

data_in = []
data_out = []
file_to_transfer = ''

def set_data_in(x):
    data_in.append(x)

def get_data_in():
    return data_in

def set_data_out(x):
    data_out.append(x)

def get_data_out():
    return data_out

def set_file_to_transfer(x):
    global file_to_transfer
    file_to_transfer = (os.path.dirname(os.path.abspath(__file__))+"\\"+x)

def get_file_to_transfer():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return file_to_transfer

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
            set_file_to_transfer(file_to_transfer)
            #return file_to_transfer
        


############### TRANSFER ###############
def transfer():
    filepath = get_file_to_transfer()
    f = open(filepath, "r")
    lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        print("Line {}: {}".format(count, line))
        ser.write(line.encode())
        time.sleep(0.1)

############### RECEIVE ###############

def receive():
    #while ser.in_waiting:
    end_of_file = ("#END\r")                #end of file as dictated by PIC code, this is added by default to files generated through SID-Automation-GUI
    data = ser.read_until(end_of_file)
    set_data_in(data)
    
def receive_all():
    data = ser.read_all()
    print(data)
    set_data_in(data)

def transmit(cmd_to_transmit):
    data = str.encode(cmd_to_transmit)
    ser.write(data)
    #ser.write(data_out)
    #for x in range(len(data)):
    #    print(data(x))
    #    set_data_out(data[x])

############### MAIN ###############
ser = serial.Serial(com_check(), 9600, timeout=0.050)       # hard-coding to 9600 baud since that's what MS-SID uses, expand this later if used for other projects
wait_time = 1 # in seconds, i found that anything too fast didn't give the PIC enough time to respond to commands, this may matter more for RCFG
file_name = 'msoperat.cfg' #currently MS-SID code only expects this filename but making it variable in case that changes in future

file_selection()
transmit('QUIT\r\n') # get out of file operations menu if there
time.sleep(wait_time)
receive_all()
#transmit('RCFG\r\n')
#time.sleep(0.2)
#receive_all()
#transmit('*\r\n')
#time.sleep(0.2)
#receive_all()
transmit('FILE\r\n')
time.sleep(wait_time)
receive_all()
#transmit('COPY CON ' + 'file_name' + '\r\n')   # open file msoperat.cfg to write
transmit('COPY CON msoperat.cfg\r\n')   # open file msoperat.cfg to write
time.sleep(wait_time)
receive_all()
transfer()      # transfer data to write
time.sleep(wait_time)
receive_all()
transmit('\032\r\n')    # ascii control z to exit COPY CON