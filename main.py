from kivy.app import App
from kivy.uix.widget import Widget

class DataloggerMain(Widget):
    def mensaje(self, evento):
        print("CLICK")
        print(evento)
    #def on_touch_down(self, argumento):
    pass

class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

