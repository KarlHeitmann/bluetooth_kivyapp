from kivy.app import App
from kivy.uix.widget import Widget

class DataloggerMain(Widget):
    pass

class DataloggerApp(App):
    def build(self):
        return DataloggerMain()

if __name__ == '__main__':
    DataloggerApp().run()

