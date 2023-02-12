from Crypto.Cipher import AES
from Crypto import Random
#from Crypto.Random import random

def aes_encrypt(plaintext, k):
    #print(random.randrange(5,5,5))
    #return iv + ciphertext (in bytes)
    #k = k.encode("utf8")
    #plaintext = plaintext.encode("utf8")
    # print(len(plaintext))
    #print(plaintext.title())

    b_plaintext = bytearray(plaintext)
    while(len(b_plaintext) % 16 != 0):
        b_plaintext.append(0)

    IV = Random.get_random_bytes(16)
    cipher = AES.new(k, AES.MODE_CBC, IV=IV)
    ciphertext = cipher.encrypt(b_plaintext)
    return IV + ciphertext

def aes_decrypt(ciphertext, k):
    # return plaintext (in 'latin1')
    IV = ciphertext[0:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(k, AES.MODE_CBC, IV=IV)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


#### ENCRYPT THE PDF FILE
# pdf_file = open("test.pdf", "rb")
# encrypted_pdf_file = aes_encrypt(pdf_file.read(), b"0360001110000000")
# pdf_file.close()

# enc_pdf_file = open("enc.pdf", "wb")
# enc_pdf_file.write(encrypted_pdf_file)
# enc_pdf_file.close()

#### DECRYPT THE PDF FILE
enc_pdf_file = open("enc.pdf", "rb")
decrypted_pdf_file  = aes_decrypt(enc_pdf_file.read(), b"0360001110000000")
enc_pdf_file.close()

dec_pdf_file = open("dec.pdf", "wb")
dec_pdf_file.write(decrypted_pdf_file)
dec_pdf_file.close()
