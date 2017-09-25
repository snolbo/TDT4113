import crypto_utils
import random
import itertools

class Cipher:
    ALPHABETH_SIZE = 95;
    ALPHABETH = [chr(x) for x in range(32,127)]

    def __init__(self):
        self.key = None
        return

    def encode(self, clear_text):
        return

    def decode(self, cipher_text):
        return

    def verify(self, clear_text, decoded_text):
        return clear_text == decoded_text

    def generate_keys(self):
        return

    def possible_keys(self):
        return

    def set_key(self, key):
        self.key = key
        return

    def get_key(self):
        return self.key









class Caesar(Cipher): # DONE
    def __init__(self):
        super(Caesar, self).__init__()
        return


    def encode(self, clear_text):
        encoded_text = ""
        for char in clear_text:
            index = self.ALPHABETH.index(char)
            index = (index + self.key) % self.ALPHABETH_SIZE
            encoded_text += self.ALPHABETH[index]
        return encoded_text

    def decode(self, cipher_text):
        decoded_text = ""
        for char in cipher_text:
            index = self.ALPHABETH.index(char)
            index =  (index + self.ALPHABETH_SIZE - self.key) % self.ALPHABETH_SIZE
            decoded_text += self.ALPHABETH[index]
        return decoded_text

    def generate_keys(self):
        return

    def possible_keys(self):
        return range(0, self.ALPHABETH_SIZE)



class Multiplicative(Cipher): # done

    def __init__(self):
        return

    def encode(self, clear_text):
        encoded_text = ""
        for char in clear_text:
            index = self.ALPHABETH.index(char)
            index = index*self.key % self.ALPHABETH_SIZE
            encoded_text += self.ALPHABETH[index]
        return encoded_text

    def decode(self, cipher_text):
        decoded_text = ""
        for char in cipher_text:
            index = self.ALPHABETH.index(char)
            inv =  crypto_utils.modular_inverse(self.key, self.ALPHABETH_SIZE)
            index= index*inv % self.ALPHABETH_SIZE
            decoded_text += self.ALPHABETH[index]
        return decoded_text

    def generate_keys(self):
        return

    def set_key(self, key):
        inv = crypto_utils.modular_inverse(key, self.ALPHABETH_SIZE)
        if inv*key % self.ALPHABETH_SIZE == 1:
            super(Multiplicative, self).set_key(key)
        else:
            print("This key does not have a modular inverse, and cannot be used. Crash incoming...")
            return

    def possible_keys(self):
        possible_keys = []
        for i in range(0, self.ALPHABETH_SIZE):
            inverse = crypto_utils.modular_inverse(i, self.ALPHABETH_SIZE)
            if i*inverse % self.ALPHABETH_SIZE == 1: #i has inverse modulo, hence possible key
                possible_keys.append(i)
        return possible_keys






class Affine(Cipher):

    def __init__(self):
        self.mult_cipher = Multiplicative()
        self.cae_cipher = Caesar()

    def set_key(self, key):
        self.key = key
        self.mult_cipher.set_key(key[0])
        self.cae_cipher.set_key(key[1])

    def encode(self, clear_text):
        encoded_text = clear_text
        encoded_text = self.mult_cipher.encode(clear_text)
        encoded_text = self.cae_cipher.encode(encoded_text)
        return encoded_text


    def decode(self, cipher_text):
        decoded_text = cipher_text
        decoded_text = self.cae_cipher.decode(decoded_text)
        decoded_text = self.mult_cipher.decode(decoded_text)
        return decoded_text

    def generate_keys(self):
        return

    def possible_keys(self):
        possible_shifts = self.cae_cipher.possible_keys()
        possible_factors = self.mult_cipher.possible_keys()
        possible_keys = itertools.product(possible_factors, possible_shifts)
        return possible_keys



class Unbreakable(Cipher): # Done
    def __init__(self):
        return

    def set_key(self, key):
        super(Unbreakable, self).set_key(key)
        self.key_len = len(key)

    def encode(self, clear_text):
        encoded_text = ""
        i = 0
        for char in clear_text:
            clear_text_index = self.ALPHABETH.index(char)
            key_char = self.key[i % self.key_len]
            key_index = self.ALPHABETH.index(key_char)
            encoded_text += self.ALPHABETH[(clear_text_index + key_index) % self.ALPHABETH_SIZE]
            i += 1
        return encoded_text


    def decode(self, cipher_text):
        decoded_text = ""
        i = 0
        for char in cipher_text:
            key_char = self.key[i % self.key_len]
            key_index = (self.ALPHABETH_SIZE - self.ALPHABETH.index(key_char)) % self.ALPHABETH_SIZE
            cipher_char_index = self.ALPHABETH.index(char)
            decoded_text += self.ALPHABETH[(cipher_char_index + key_index) % self.ALPHABETH_SIZE]
            i += 1
        return decoded_text

    def generate_keys(self):
        return

    def possible_keys(self, max_key_len = 2):
        possible_keys = []
        for key_len in range(1, max_key_len +1):
            for subset in itertools.permutations(self.ALPHABETH, key_len):
                possible_keys.append(''.join(subset))
        return possible_keys


class RSA(Cipher): # not correct
    def __init__(self, bits):
        self.bits = bits
        self.public_key = None
        self.private_key = None
        self.generate_keys()
        return

    def encode(self, clear_text):
        encoded_list = []
        blocks_from_text = crypto_utils.blocks_from_text(clear_text, 1)
        for block in blocks_from_text:
            number = pow(block, self.public_key[1], self.public_key[0])
            encoded_list.append(number)
        return encoded_list


    def decode(self, encoded_list):
        decoded_list = []
        for num in encoded_list:
            decoded_number = pow(num, self.private_key[1], self.private_key[0])
            decoded_list.append(decoded_number)
        decoded_text = crypto_utils.text_from_blocks(decoded_list, self.bits)
        return decoded_text

    def generate_keys(self):
        while True:
            p = crypto_utils.generate_random_prime(self.bits)
            q = crypto_utils.generate_random_prime(self.bits)
            if p != q:
                break
        print("Primes choosen")
        print("random prime1: " + str(p))
        print("random prime2: " + str(q))
        n = p *q
        phi = (p-1)*(q-1)
        print("phi : " + str(phi) + " n: " + str(n))
        while True:
            e = random.randrange(3, phi -1, 2)
            d = crypto_utils.modular_inverse(e, phi)
            if (e*d)% phi == 1: # ensures decoding is unique
                break
        self.public_key = (n,e)
        self.private_key = (n,d)
        print("public key: " + str(self.public_key))
        print("private key: " + str(self.private_key))
        return


    def possible_keys(self, max_key_len = 2):
        possible_keys = []
        for key_len in range(1, max_key_len +1):
            for subset in itertools.permutations(self.ALPHABETH, key_len):
                possible_keys.append(''.join(subset))
        return possible_keys
