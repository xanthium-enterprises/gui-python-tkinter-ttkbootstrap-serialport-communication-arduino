#=======================================================================#
# Python tkinter (ttkbootstrap) based GUI Serial Communication Program  #
# (c) 2026 www.xanthium.in                                              #
# Rahul.S                                                               #
#=======================================================================#


import ttkbootstrap as ttkb
from tkinter import *
from ttkbootstrap.scrolled import ScrolledText # import the scrolled text box 
                                               # ttkbootstrap.scrolled.ScrolledText
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk 

import serial
import platform

from datetime import datetime
import time

#================================================================================#
# this function opens the serial port and send and receive data to arduino       #
#================================================================================#
def serial_arduino_send_receive():
    
    port_number = com_port_number_entry_box.get() # read the port number from entry box
    baudrate    = int(baudrate_combo.get())       # read the baud rate from combo box
                                                  # convert baudrate string to int
    received_data_entry.delete(0,tk.END)
    
    try:
        serial_port_object = serial.Serial(port_number,baudrate) # open the serial port 
        serial_port_object.timeout  = 3                          # Setting Read timeouts here
        
    except serial.SerialException as var :
        print('An Exception Occured')
        print('Exception Details-> ', var)
        Messagebox.show_error(title='Serial Exception Occured', message=f'{var}' )
        
    else:
               
        print(f'Serial Port {serial_port_object} Opened')
        
        log_data.insert(END,f'\n Serial Port {serial_port_object.name} Opened') # Write to the scrolled textbox log 
        log_data.insert(END,f'\n Baud Rate = {serial_port_object.baudrate}\n ')
        
        data_to_be_transmited = transmit_data_button_entry_box.get()      # get the character to be transmitted from th entry box 
        data_to_be_transmited = bytearray(data_to_be_transmited, "utf-8") # convert string to byte array as pyserial write() requires byte array
        
        log_data.insert(END,f'\n A 2 second delay for  Arduino to stabilize ')
        time.sleep(2) # this delay is for Arduino only,once you open the serialport -
                      # - Arduino gets Resetted
        
        
        serial_port_object.write(data_to_be_transmited) # send the character to Arduino
        
        print(data_to_be_transmited) 
        log_data.insert(END,f'\n {data_to_be_transmited} Transmitted ')
        
        
        #serial_port_object.reset_input_buffer()
        #time.sleep(0.5)
        
        received_data_entry.delete(0,tk.END) #clear the received_data_entry box 
        
        received_data =  serial_port_object.readline()         # read the data from serial port 
        received_data =  received_data.decode("utf-8").strip() # readline() returns bytes which we need to be converted back to string
                                                               # .strip() removes the \r\n send by the Arduino
        print(received_data)
               
        log_data.insert(tk.END,f'\n {received_data} Received ')
        log_data.see(tk.END) #ensures that cursor is positioned at last entry (auto scrolling)
        
        received_data_entry.insert(0,received_data) #display received data 
        
        serial_port_object.close() # close the serial port  
    
#========================================================================#
#                        GUI Handler Functions                           #
#========================================================================#

def transmit_data_button_handler():
    print('You Clicked Transmit Button')
    serial_arduino_send_receive() # main function that does all the serial tx/rx comm
    
def baudrate_combobox_selected_handler(e):
    print(e)
    

#========================================================================#
# GUI Creation Code                                                      #
#========================================================================#

root = ttkb.Window(themename = 'superhero') # theme = superhero

#root = ttkb.Window(themename = 'cosmo') # theme = cosmo
#root = ttkb.Window(themename = 'darkly') # theme = darkly
#root = ttkb.Window(themename = 'solar') # theme = flatly

root.geometry('470x520')                            # width x height
root.title('Python Serial Port Communication')      # name of window

root.resizable(0,0) # Disable resizing in all directions,Maximize button disabled
                    # root.resizable(x,y)
                
                    
com_port_name_label = ttkb.Label(text = 'Serial Port No')
com_port_name_label.place(x=20,y=30)

# Create COM Port number Entry Widget 
com_port_number_entry_box = ttkb.Entry()

com_port_number_entry_box.place(x=125,y = 25)

baud_rate_label = ttkb.Label(text = 'Baud Rate')
baud_rate_label.place(x=25,y=80)

# Baud rate selection Combobox 
std_baudrate = ['1200','2400','4800','9600','19200','38400','57600','115200'] # std baudrate options for serial comm
                                                                              # these are text,convert to int

baudrate_combo = ttkb.Combobox(values = std_baudrate) # Pass std_baudrate list to combobox
baudrate_combo.current(3)                             # set 9600 as default
baudrate_combo.bind('<<ComboboxSelected>>',baudrate_combobox_selected_handler) # bind the combobox
baudrate_combo.place(x=125,y=75)


#Create a Button
transmit_data_button = ttkb.Button(text = 'Transmit Data',bootstyle="danger",command = transmit_data_button_handler)
transmit_data_button.place(x=25,y=150)

#Create Transmit data Entry Widget 
transmit_data_button_entry_box = ttkb.Entry()
transmit_data_button_entry_box.insert(0,'')   #Clear the Transmit data Entry Box 
transmit_data_button_entry_box.place(x=155,y = 150)

#Receive Data Widget
received_data_entry = ttkb.Entry()
received_data_entry.place(x=155,y = 200)

received_data_label = ttkb.Label(text = 'Received Data',bootstyle="success")
received_data_label.place(x=30,y=205)

# log data
log_data_label = ttkb.Label(text = 'Logging')
log_data_label.place(x=25,y=245)

log_data = ScrolledText(root,height = 10,width = 50,wrap = WORD)
log_data.place(x=25,y=272)
log_data.insert(tk.END,f'OS    :  {platform.platform()}\n')# add text
log_data.insert(tk.END,f'Time :  {datetime.now()}\n')

# website
website = ttkb.Label(text = 'www.xanthium.in')
website.place(x=25,y=490)

root.mainloop()

