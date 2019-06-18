import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

import argparse

BLUETOOTH_MODULE = True
#BLUETOOTH_NAME = 'ESP32Playground'
BLUETOOTH_NAME = 'ESP32test'

if 'BLUETOOTH_OFF' in os.environ:
    BLUETOOTH_MODULE = False
    print("APAGADO bluetooth")
    print(BLUETOOTH_MODULE)

if BLUETOOTH_MODULE:
    from btdriver import get_socket_stream, myThread


class Driver():
    def __init__(self, dsa):
        print(dsa)
    def inicializar(self, datalogger_main):
        print("inicializando")
        if BLUETOOTH_MODULE:
            self.recv_stream, self.send_stream = get_socket_stream(BLUETOOTH_NAME)
            self.input_thread = myThread(datalogger_main, 1, "Thread-1", 1, self.recv_stream)
            self.input_thread.start()
    def enviar(self):
        print("ENVIANDO...")
        if BLUETOOTH_MODULE:
            self.send_stream.write("{\"datum\":{\"potencia\":99.9}}\n".encode())
    def attach(self, datalogger_main):
        self.datalogger_main = datalogger_main
        print("ATTACHED")
        self.datalogger_main.callback_bluetooth_rx("!")

class DataloggerMain(BoxLayout):
    '''
    def __init__(self):
        self.random_number = StringProperty()
        self.bt_driver = Driver("asddsa")
        self.init_msg()
        self.bt_driver.inicializar()
        super(DataloggerMain, self).__init__()
    '''
    random_number = StringProperty()
    conectar = False
    if BLUETOOTH_MODULE:
        bt_driver = Driver("asddsa")
    def mensaje(self, evento):
        if self.conectar:
            self.random_number = "WENA"
            if BLUETOOTH_MODULE:
                print(self.bt_driver)
                self.bt_driver.enviar()
            print("CLICK")
            print(evento)
        else:
            if BLUETOOTH_MODULE:
                self.bt_driver.inicializar(self)
            self.conectar = True
    #def on_touch_down(self, argumento):
    def init_msg(self):
        print("hfdkjhgf dgf djkg dfg dfkgdf")
    def callback_bluetooth_rx(self, texto):
        print("HOLA MUNDO!")
        self.random_number = texto


class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

