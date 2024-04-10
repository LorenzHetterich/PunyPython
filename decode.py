import sys
print((b"\n" + b"\n".join(open(sys.argv[1], "rb").read().split(b"\n")[1:])).decode("punycode"))
