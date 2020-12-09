from cryptography.fernet import Fernet
import random
import string
import base64
import os

lda5148_gds187 = 'gAAAAABdLHawh8-ODLRD4U6DFN1DyhP7b-wLN5D7jX5QEoDqXR6Mfar2nwPpltUzVO39B5QTb9RIRiT_8f0dBRdMKWBqU195EEEBegWBzNfFXxq8bJs_Dc0='
lda5148_api = 'gAAAAABea1RJW0spbTGvXCAewqmg83gMQ19lbUag-otUBuz0evyarW44ZIr7hbT0o864jLonhhI-x1czKc0KvF0lH4OiWagSYqoQqKqrP2R__wqnr32Awvw='
lda5148_aws_aki = 'gAAAAABc9ho5QIDsC_YIbWKSF7TXBcUnKqYRxxwQPxIGIl4e0cmszXkX0ubVHjKOfFZF74ySTlx9IizkyLGmJngqQaiAotrXWRdWEkq02uZHTw2Ka2s6v90='
lda5148_aws_sak = 'gAAAAABc9ho5u8R8o3bxPG_-wPrYsNTHWr2HOKYFoHVUWvnZdXZugvJn3kSXvoKG2YMl3g7NpDlXhimEouUr5fe3lnDBPcy-ucsZ5cBHzzAeBCHB3TBQQO2Dq3fdSs7aXBe0_LRJNsLJ'


def generate_random_alphanumeric_key(length: int = 20):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))


def decrypt(data):
    key = os.environ['DSA_CRYPTO_KEY'].encode('utf-8')
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(data.encode('utf-8')).decode('utf-8')


def encrypt(data):
    key = os.environ['DSA_CRYPTO_KEY'].encode('utf-8')
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.encrypt(data.encode('utf-8')).decode('utf-8')
