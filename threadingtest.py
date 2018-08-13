import can
from queue import Queue
from threading import Thread
from dataAcquisition import *
from lib import startupCheck
from lib import ExceptionHandling
from lib import CanMessages
from kivy.app import App
#from RGBColorMap import *
from kivy.metrics import pt
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang.builder import Builder
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

os.environ['KIVY_DPI'] = '188'  #Set the screen resolution so that fonts scale correctly

CONFIG_FILE_PATH = '/media/usb0/config.ini'
RGBCOLORMAP_FILE_PATH = '/media/usb0/RGBColorMap.txt'
DEBUG_PRINT = True

Builder.load_string('''
<Label>:
    font_name: "Arial"
    size_hint: (None,None)
    size: self.texture_size
    font_size: 75
    pos: (0,0)
''')
  
def debugPrint(string):
    if DEBUG_PRINT:
        print(string)

        
class MainApp(App):
    
    _layout = None #This holds the layout widget
    _labels = [None]*20 #This holds all the labels
    _images = [None]*20 #This holds all of the images
    _worker_thread = None #Holder for the worker thread object
    _worker_queue = None #This holds the queue for commmunicating with the worker thread
    _string_messages = None #Place holder for the string messages object

    
    
    def build(self):    #Build and return the layout widget
        
        self._layout = FloatLayout(size = (800,480))    #Create the layout, the size of the screen
        #self._worker_queue = Queue()    #Create worker queue
        
        self._worker_thread = threading.Thread(target = self._worker, args = ()) #Create the thread object
        self._worker_thread.setDaemon(True) #Set the worker thread as a daemon, since it never returns
        self._worker_thread.start() #Start the worker thread
        print("Returned from thread")
        return self._layout
    
    def on_start(self):   #On start, create the queue and threads
        
        # #self._worker_queue = Queue()    #Create worker queue
        
        # self._worker_thread = threading.Thread(target = self._worker, args = ()) #Create the thread object
        # self._worker_thread.setDaemon(True) #Set the worker thread as a daemon, since it never returns
        # self._worker_thread.start() #Start the worker thread
        
        Clock.schedule_interval(self._displayFunc, 0.1)
    


    @mainthread
    def _worker(self):
        
        self._worker_queue = Queue()    #Create worker queue
        bus = CanMessages.CANInit(systemParams.canRate)
        CanMessages.setupGPIO()
        
        
        a_listener = can.BufferedReader()   #Create a listener
        notifier = can.Notifier(bus,[a_listener])   #Create a notifier
        print("NOTIFIER DONE")
        _string_messages = CanMessages.StringData()
        
        while True:
            print("IN WHILE")
            m = a_listener.get_message(0.25)    #Check to see if a message was received
            if m is not None:   #If no message received, "None" is returned

                message = m.data
                message = CanMessages.reverseByteOrder(message)
                self._worker_queue.put(message, True)  

            getThrottle()
            getSteering()


  
    def _displayFunc(self,delta_time):
        pass
        
        # # canData = self._worker_queue.get()
        # # self._worker_queue.task_done()
            
        # ID = CanMessages.determineMessageType(canData)
            
        # if ID == 22 and stringMsg.inProcess is False:
            # if self._labels[strData.stringID] is None: #Check if the label doesnt already exist
                # colors = getRGBValues(strData.color)
                # self._labels[strData.stringID] = Label(text=strData.string, size_hint = (None, None), pos = (strData.posX,strData.posY),font_size=pt(strData.size), color = (colors[0]/255,colors[1]/255, colors[2]/255,1))#,halign="left",valign="bottom")
                # self._labels[strData.stringID].size = self._labels[strData.stringID].texture_size
                # strData.string = ""
                # self._layout.add_widget(self._labels[strData.stringID])

        # if ID == 23:
            # if self._labels[strData.stringID] is not None:
                # self._layout.remove_widget(self._labels[strData.stringID])
                # self._labels[strData.stringID] = None


if __name__ == "__main__":
    MainApp().run()


