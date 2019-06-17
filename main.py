from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

import threading
import time

from jnius import autoclass

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    print("========================")
    print([ x.getName() for x in paired_devices ])
    print(paired_devices)
    socket = None
    for device in paired_devices:
        print(device.getName())
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    return recv_stream, send_stream


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, inputStream):
        threading.Thread.__init__(self)
        self.inputStream = inputStream
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        counter = 5
        mensaje = ""
        while counter:
            if (self.inputStream.available()):
                input_chr = chr(self.inputStream.read())
                mensaje = mensaje + input_chr
                if (input_chr == '\n'):
                    print(mensaje)
                    mensaje = ""
            '''
            data_in = self.inputStream.available()
            buffer_array = []
            if (data_in):
                byte_string = self.inputStream.read(buffer_array)
                print(byte_string)
                print(buffer_array)
                data_in = 0
                #print(byte_string.decode())
            #print(self.inputStream)
            '''
        print_time(self.name, self.counter, 5)
        print ("Exiting " + self.name)

class Driver():
    def inicializar(self):
        print("inicializando")
        self.recv_stream, self.send_stream = get_socket_stream('ESP32test')
        self.input_thread = myThread(1, "Thread-1", 1, self.recv_stream)
    def enviar(self):
        print("ENVIANDO...")
        self.send_stream.write("{\"datum\":{\"potencia\":99.9}}\n".encode())

class DataloggerMain(Widget):
    random_number = StringProperty()
    bt_driver = Driver()
    bt_driver.inicializar()
    def mensaje(self, evento):
        self.random_number = "WENA"
        print(self.bt_driver)
        self.bt_driver.enviar()
        print("CLICK")
        print(evento)
    #def on_touch_down(self, argumento):
    pass

class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

