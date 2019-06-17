from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class DataloggerMain(Widget):
    random_number = StringProperty()

    def mensaje(self, evento):
        self.random_number = "WENA"
        print("CLICK")
        print(evento)
    #def on_touch_down(self, argumento):
    pass

class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

