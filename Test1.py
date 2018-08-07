from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import pigpio

pi = pigpio.pi()



class mainApp(App):

    _layout = None #This holds the root layout widget

    _labels = [None] #This will hold all our labels


    def build(self):

        #Create the layout to hold all the widgets
        self._layout = FloatLayout(size = (800, 480))

        return self._layout

    def on_start(self):

        #Schedule a timer
        Clock.schedule_interval(self._update, 0.1)


    def _update(self, delta_time):

        #If GPIO40 is triggered, add the widget
        if pi.read(40):
            self._labels[0] = Label(text="Hello!", font_size=150)
            self._layout.add_widget(self._labels[0],0)

        #If GPIO41 is triggered, remove the widget
        if pi.read(41):
            self._layout.remove_widget(self._labels[0])


if __name__ == "__main__":
    main_app = mainApp()

    main_app.run()
