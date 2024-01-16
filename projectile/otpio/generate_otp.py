import random

def otp_generator(length=6):
    otp = ''.join([str(random.randint(0, 9)) for i in range(length)])

    return otp