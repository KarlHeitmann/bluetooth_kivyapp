import kivy
from kivy.app import App
from kivy.uix.label import Label

import threading
import time

# Same as before, with a kivy-based UI

'''
Bluetooth/Pyjnius example
=========================
This was used to send some bytes to an arduino via bluetooth.
The app must have BLUETOOTH and BLUETOOTH_ADMIN permissions (well, i didn't
tested without BLUETOOTH_ADMIN, maybe it works.)
Connect your device to your phone, via the bluetooth menu. After the
pairing is done, you'll be able to use it in the app.
'''

from jnius import autoclass


BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

exit_flag = 0

def print_time(threadName, delay, counter):
    while counter:
        #if exitFlag:
        #    threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

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

if __name__ == '__main__':
    from kivy.lang import Builder
    from kivy.app import App

    class Bluetooth(App):
        def build(self):
            #self.recv_stream, self.send_stream = get_socket_stream('linvor')
            self.recv_stream, self.send_stream = get_socket_stream('ESP32test')
            self.input_thread = myThread(1, "Thread-1", 1, self.recv_stream)
            self.input_thread.start()
            return Builder.load_string(kv)

        def send(self, cmd):
            #self.send_stream.write('{}\n'.format(cmd))
            self.send_stream.write("{\"datum\":{\"potencia\":99.9}}\n".encode())
            print(cmd)
            print(self.send_stream)
            #self.send_stream.write(cmd.encode())
            #self.send_stream.write("")
            self.send_stream.flush()

        def reset(self, btns):
            for btn in btns:
                btn.state = 'normal'
            self.send('0\n')

    Bluetooth().run()


if __name__ == "__main__":
    MyApp().run()

