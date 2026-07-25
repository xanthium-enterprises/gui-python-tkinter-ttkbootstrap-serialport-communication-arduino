import serial
import time

data_txed = b'a'

serial_port_object = serial.Serial('COM3',9600)
time.sleep(2)

serial_port_object.write(data_txed)
time.sleep(1)

received_data =  serial_port_object.readline()

print(received_data)

serial_port_object.close()


