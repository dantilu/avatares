# -*- coding: utf-8 -*-
# !/usr/bin/python
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from ciberinteligencia.configuration.config import INTERRUPT, BLOCK_SIZE, PAD, SECRET_KEY, IV

cipher_for_encryption = None
cipher_for_decryption = None


def encrypt_with_aes(encrypt_cipher, plaintext_data):
    plaintext_padded = add_padding(plaintext_data, INTERRUPT, PAD, int(BLOCK_SIZE))
    encrypted = encrypt_cipher.encrypt(plaintext_padded)
    return b64encode(encrypted)


def decrypt_with_aes(decrypt_cipher, ciphered_data):
    decoded_encrypted_data = b64decode(ciphered_data)
    decyphered_data = decrypt_cipher.decrypt(decoded_encrypted_data)
    return strip_padding(decyphered_data, INTERRUPT, PAD)


def add_padding(data, interrupt, pad, block_size):
    new_data = ''.join([data, interrupt])
    new_data_len = len(new_data)
    remaining_len = block_size - new_data_len
    to_pad_len = remaining_len % block_size
    pad_string = pad * to_pad_len
    return ''.join([new_data, pad_string])


def strip_padding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt)


try:
    cipher_for_encryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    cipher_for_decryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    #print encrypt_with_aes(cipher_for_encryption, 'M84smbOl6pVWh0mWETshejWet')
    #print encrypt_with_aes(cipher_for_encryption, 'zW8r6nr0UExbjZ6yNqUpAh86FBBE7dPaxSBB0Dvzo7WWDfrHwI'+'000')
    #print encrypt_with_aes(cipher_for_encryption, '963171395701264385-6MiOLwBA5lJj6In5uHzTBNhNgheK1h5'+'000')
    #print encrypt_with_aes(cipher_for_encryption, 'Nfpe2hZKknxdioQgzd1LjwkhQN0zBW6ppB3hrYkNq7zX6')

    #print decrypt_with_aes(cipher_for_decryption, 'xtXWF1E2tthbAidq1F/uYHMbCtukisOcWcmWBvBQvE+Y6qb8IBvKNcNgqBwnWOQPupecj0DBpWP5fmGDQLdce+qt468Wvsm8+oiTdz3mKxQF8NHmzXuUI5VoPHtpKaAki4DLUVYljdCdf+zFBb5ZaIZjE1sf7ejytwUo2t72LlRH/XjuHGjcns+cv5ioLqMEQG89i+121CmqUY/uYmJgKTW4cjLoetrxrZSN6qptU1cJGOAQZEU6busGNCAVhMDlTaA2Chk5S42nlqWiA1o3SWAXYO5y8pQa1JLRrJFtddV5YPRm5SprovIP371r3jv8plkqEy/QzcTgQBjVY7zxkxgDgFKPWIVOoCgwELbA8vWYPSkU/cGxJ3B7jk8I1duyE5QsHFe1CuIhvWIO5qMvHw==')
    #print decrypt_with_aes(cipher_for_decryption, '3bPpvrmBmuazqoj2Q+NtyXvkMbUtIw5111yo4njBfoDL74hT/NUMm3Bk1yxCmgh5HHY4cuCPTnKMPKtc/yrAbvCRGS05kWo0SCMOLp4RHBc=')
    #print decrypt_with_aes(cipher_for_decryption, '26MvxTjPoNatyjcN+l49TPDvqO92BVqlpCbtttDMsoDaJZrsgtrud9Nr2HelWbnAxRT9bIpAbaTyXdYJxIO8ahOT2C6JVzJ5XuwjEOjvGXU=')
    #print decrypt_with_aes(cipher_for_decryption, 'I4FW3OsQvD+ZjQ6aUOqeIuMh0lQJQseux8cVEsxqXjZYxGYTFXZl6u21FMolA9UH5+xquEEs1zLx2Bt2z69u8h42mgo/u0SquPFpvFNOcbqyIBWEJa3cp9EYmRfyJ+oz2l46tiSFqyAY6L5GBmh6Y5a+PYJ7l6XHBNE/RwJEHES9Y9OCClqUJQUqQ6b7GjsV')


except Exception as e:  # catch all those ugly errors
    print "Error AES.py {}".format(e)
