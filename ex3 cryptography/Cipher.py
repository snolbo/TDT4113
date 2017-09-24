import crypto_utils

class Cipher:
    ALPHABETH_SIZE = 95;
    ALPHABETH = [chr(x) for x in range(32,127)]

    def __init__(self):
        return

    def encode(self, clear_text):
        return

    def decode(self, cipher_text):
        return

    def verify(self, clear_text, decoded_text):
        return clear_text == decoded_text

    def generate_keys(self):
        return





class Caesar(Cipher): # DONE

    def __init__(self, right_shift):
        self.right_shift = right_shift


    def encode(self, clear_text):
        encoded_string = ""
        for char in clear_text:
            index = self.ALPHABETH.index(char)
            index = (index + self.right_shift) % self.ALPHABETH_SIZE
            encoded_string += self.ALPHABETH[index]
        return encoded_string

    def decode(self, cipher_text):
        decoded_string = ""
        for char in cipher_text:
            index = self.ALPHABETH.index(char)
            index =  (index + self.ALPHABETH_SIZE - self.right_shift) % self.ALPHABETH_SIZE
            decoded_string += self.ALPHABETH[index]
        return decoded_string

    def generate_keys(self):
        return



class Multiplicative(Cipher):

    def __init__(self, factor):
        self.factor = factor

    def encode(self, clear_text):
        encoded_string = ""
        for char in clear_text:
            index = self.ALPHABETH.index(char)
            index = index*self.factor % self.ALPHABETH_SIZE
            encoded_string += self.ALPHABETH[index]
        return encoded_string
        return

    def decode(self, cipher_text):
        decoded_string = ""
        for char in cipher_text:
            index = self.ALPHABETH.index(char)
            a =  crypto_utils.modular_inverse(self.factor, self.ALPHABETH_SIZE)
            index= index*a % self.ALPHABETH_SIZE
            decoded_string += self.ALPHABETH[index]
        return decoded_string

    def generate_keys(self):
        return


class Affine(Cipher):

    def encode(self, clear_text):
        return

    def decode(self, cipher_text):
        return

    def generate_keys(self):
        return

