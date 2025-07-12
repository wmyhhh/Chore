# strings are objects
s = 'Hello'
print(s.upper())
print(s.lower())
print(s.swapcase())

# representing strings: ASCII
# american standard coding information interchange
a = 'B'
print(ord(a))
print(hex(ord(a)))
print('\n\n\n')
print('\a\a\a')

# representing strings: UNICODE!
from unicodedata import name, lookup
print(name('饬'))
print(lookup('WHALE'))
print(lookup('GORILLA'))
print(lookup('ORANGUTAN'))
print(lookup('MONKEY'))
print(lookup('PARROT'))