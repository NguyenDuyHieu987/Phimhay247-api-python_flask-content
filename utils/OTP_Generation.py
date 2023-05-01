import math, random

# import smtplib

# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()


def generateOTP(length=6):
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(length):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
