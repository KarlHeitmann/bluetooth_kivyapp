from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

import threading
import time

from btdriver import get_socket_stream, myThread


class Driver():
    def inicializar(self):
        print("inicializando")
        self.recv_stream, self.send_stream = get_socket_stream('ESP32test')
        self.input_thread = myThread(1, "Thread-1", 1, self.recv_stream)
        self.input_thread.start()
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

