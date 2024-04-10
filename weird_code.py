#They say codying is fun, but I like puns, so when I code, coding!=funnycode, but coding=punycode! ... anyways, here is some nice python code :)

I="I"
love="love"
python="python"

print(I, love, python)

# shift cipher!
def shift_cipher(s, key):
    return ("".join(chr((ord(c) + key) % 128) for c in s))

# this string is super secret, so I encrypted it!
secret="ymnx%nx%f%xjhwjy%rjxxflj&"

print(shift_cipher(secret, -5))

# I love python comments, so I put one more here with some crap <3:
# here is some crap: -47415qpygaa76ea29ah9daca59abba63qeacaacc99aad01ba90babbc80bf52ba42j1lla61b70aqa632n6a49a6a40b9a19aedb39aaead4agc17j4lb81kao43bip4nlafc6b63awaf14bvobfo1b48ac55bmava93bjap79km616kt0aa689f