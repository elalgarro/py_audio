from pynput.keyboard import Key, Listener

class MyListener(Listener) : 

    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        if key.char == 'r':
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key.char == 'r':
            self.key_pressed = False
        return True

