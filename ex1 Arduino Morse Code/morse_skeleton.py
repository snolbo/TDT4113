'''This file provides a few of the 'tricky' elements of the Morse Code project: those
involving setting up and reading from the serial port.  

IMPORTANT!! If you are a MAC user, you will need to modify the actual device code for 
your serial port in arduino_connect.py '''

import arduino_connect  # This is the key import so that you can access the serial port.


# Codes for the 5 signals sent to this level from the Arduino

_dot = 0
_dash = 1
_symbol_pause = 2
_word_pause = 3
_reset = 4


# Morse Code Class
class mocoder():

# Note: the codes for dot and dash coming to Python via the serial port are 1 and 2, respectively, since those were most
# convenient at the Arduino level. However, I've switched to 0 and 1 in this dictionary, since it is a lot easier to
# read.  So O = dot, 1 = dash in the _morse_codes dictionary below.  You will need to remember that when looking
# up letters and digits in this dictionary.

    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

	# This is where you set up the connection to the serial port.
    def __init__(self,sport=True):
        if sport:
            self.serial_port = arduino_connect.pc_connect()
        self.reset()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 1-4 from the Arduino via a serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data
                
    # The signal returned by the serial port is one (sometimes 2) bytes, that represent characters of a string.  So,
    # a 2 looks like this: b'2', which is one byte whose integer value is the ascii code 50 (ord('2') = 50).  The use
    # of function 'int' on the string converts it automatically.   But, due to latencies, the signal sometimes
    # consists of 2 ascii codes, hence the little for loop to cycle through each byte of the signal.

    def decoding_loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            #print(s)
            for byte in s:
                self.process_signal(int(chr(byte))-1)
     
     # Delegates function to correct function basef on signal
    def process_signal(self,sig):
        print(sig)
        if sig == _dot or sig == _dash:
            self.update_current_symbol(sig)
        elif sig == _symbol_pause:
            self.handle_symbol_end()
        elif sig == _word_pause:
            self.handle_word_end()
        return True

    # Updates current symbol that is being recorded
    def update_current_symbol(self, sig):
        self.current_symbol += str(sig)

    # Handles the event that a pause has happened, the current symbol is translated to a letter
    def handle_symbol_end(self):
        if self.current_symbol is not '':
            if self.current_symbol in self._morse_codes:
                char_symbol = self._morse_codes[self.current_symbol]
                self.update_current_word(char_symbol)
                self.current_symbol = ''
            else:
                print("This does not correspond to any symbol, resetting dots and dashes")
                self.current_symbol = ''

    # updates current word with the given input symbol
    def update_current_word(self, symbol):
        self.current_word  += symbol
        print("Current word:   " + self.current_word)

    # Handles the event that a long time has passed between signals. Prints the word and reset for new word
    def handle_word_end(self):
        self.handle_symbol_end()
        print("-------   " + self.current_word +"   -------")
        self.current_word = ''

''' To test if this is working, do the following in a Python command window:

> from morse_skeleton import *
> m = mocoder()
> m.decoding_loop()

If your Arduino is currently running and hooked up to the serial port, then this
simple decoding loop will print the raw signals that the Arduino sends to
the serial port.  Each time you press (or release) your morse-code device, a signal should
appear in your Python window. In Python, these signals typically look like this:
 b'5' or b'1' or b'3', etc.
'''

m = mocoder()
m.decoding_loop()