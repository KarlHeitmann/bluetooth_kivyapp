from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

from btdriver import get_socket_stream, myThread


class Driver():
    def __init__(self, dsa):
        print(dsa)
    def inicializar(self, datalogger_main):
        print("inicializando")
        self.recv_stream, self.send_stream = get_socket_stream('ESP32test')
        self.input_thread = myThread(datalogger_main, 1, "Thread-1", 1, self.recv_stream)
        self.input_thread.start()
    def enviar(self):
        print("ENVIANDO...")
        self.send_stream.write("{\"datum\":{\"potencia\":99.9}}\n".encode())
    def attach(self, datalogger_main):
        self.datalogger_main = datalogger_main
        print("ATTACHED")
        self.datalogger_main.hello_world("!")

class DataloggerMain(Widget):
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
    bt_driver = Driver("asddsa")
    def mensaje(self, evento):
        if self.conectar:
            self.random_number = "WENA"
            print(self.bt_driver)
            self.bt_driver.enviar()
            print("CLICK")
            print(evento)
        else:
            self.bt_driver.inicializar(self)
            self.conectar = True
    #def on_touch_down(self, argumento):
    def init_msg(self):
        print("hfdkjhgf dgf djkg dfg dfkgdf")
    def hello_world(self, texto):
        print("HOLA MUNDO!")
        self.random_number = texto


class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

