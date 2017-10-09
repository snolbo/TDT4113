from Cipher import *
import re


class Person:

    def __init__(self):
        self.key = None
        self.algorithm = None
        return

    def set_key(self, key):
        self.algorithm.set_key(key)
        return

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        return

    def get_key(self):
        return self.algorithm.get_key()

    def operate_cipher(self):
        return



class Sender(Person):

    def operate_cipher(self, clear_text):
        return self.algorithm.encode(clear_text)


class Receiver(Person):

    def operate_cipher(self, cipher_text):
        return self.algorithm.decode(cipher_text)


class Hacker(Receiver):
    def __init__(self):
        with open('english_words.txt') as f:
            self.word_list = f.read().splitlines()
        return

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def hack(self, cipher_text):
        valid_decoded_messages = []
        possible_keys = self.algorithm.possible_keys()
        regex = "[^A-Za-z0-9 ]+" # only keep letters, numbers and spaces
        for key in possible_keys:
            self.set_key(key)
            decoded_text = self.operate_cipher(cipher_text)
            clean_text = re.sub(regex, '', decoded_text)
            clean_text = clean_text.lower()
            #print(str(self.algorithm.get_key()) + " " + decoded_text)
            list_of_decoded_words = clean_text.split()
            #print(list_of_decoded_words)
            num_valid_words = 0
            num_words = len(list_of_decoded_words)
            for word in list_of_decoded_words:
                if word in self.word_list:
                    num_valid_words += 1
            if num_valid_words/num_words > 0.6: # if x percentage of the words are in the language, add to messages
                valid_decoded_messages.append(decoded_text)
                print(key)

        return valid_decoded_messages


text = "hellow, how? !are you /doing today %%and is! not! this ?a great' evening? rubbishwordzz"
alg = Caesar()
key = "L"

p1 = Sender()
p1.set_algorithm(alg)
p1.set_key(key)

p2 = Receiver()
p2.set_algorithm(alg)
p2.set_key(p1.get_key())

cipher_text = p1.operate_cipher(text)
decoded_text = p2.operate_cipher(cipher_text)

print("Clear text: " + text)
print("encoded text sent from sender: " + str(cipher_text))
print("decoded text deciphered by receiver: " + decoded_text)
print("Verified?: " + str(alg.verify(text, decoded_text)))
print()

h = Hacker()
h.set_algorithm(alg)
valid_decoded_messages  = h.hack(cipher_text)
print()
print("Possible decoded messages:")
print(valid_decoded_messages)





