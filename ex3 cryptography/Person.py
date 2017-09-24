from Cipher import *


class Person:

    def __init__(self):
        self.key = ""
        self.algorithm = Cipher()
        return


    def set_key(self, key):
        self.key = key
        self.algorithm = Multiplicative(key)
        return

    def get_key(self):
        return self.key

    def operate_cipher(self):
        return



class Sender(Person):

    def operate_cipher(self, clear_text):
        return self.algorithm.encode(clear_text)


class Receiver(Person):

    def operate_cipher(self, cipher_text):
        return self.algorithm.decode(cipher_text)



text = "xyz"

# Trading keys
p1 = Sender()
p1.set_key(2)

p2 = Receiver()
p2.set_key(p1.get_key())

# Operating on text

encoded_text = p1.operate_cipher(text)
decoded_text = p2.operate_cipher(encoded_text)

print(text)
print(encoded_text)
print(decoded_text)









