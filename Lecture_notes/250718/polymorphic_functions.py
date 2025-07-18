# a function that applies to many forms of data
# e.g. str() repr()

'''
>>> half.__repr__()
'Fraction(1, 2)'
>>> half.__str__()
'1/2'
>>>
'''

# an instance attribute called on __repr__ is ignore
# only class attributes are found

def repr(x):
    return type(x).__repr__(x)

# interface 
# a set of shared messages, along with a specification of what they mean
# connect a bunch of classes that has similar attributes

def gcd(n, d):
    while n != d:
        n, d = min(n, d), abs(n - d)
    return n

class Ratio:
    def __init__(self, n, d):
        self.numerator = n
        self.denominator = d

    def __repr__(self):
        return 'Ratio({0},{1})'.format(self.numerator, self.denominator)
    
    def __str__(self):
        return '{0}/{1}'.format(self.numerator, self.denominator)
    
    def __add__(self, other):
        if isinstance(other, int):
            n = self.numerator + self.denominator * other 
            d = self.denominator
        elif isinstance(other, Ratio):
            n = self.denominator * other.numerator +self.numerator * other.denominator
            d = self.denominator * other.denominator
        elif isinstance(other, float):
            return other + float(self)
        g = gcd(n, d)
        return Ratio(n/g, d/g)
    
    def __radd__(self, other):
            return self.__add__(other)
    def __float__(self):
        return self.numerator / self.denominator
'''
>>> a = Ratio(1, 3)
>>> b = Ratio(3, 17)
>>> c = 2
>>> d = 6.77
>>> str(a.__add__(b))
'26.0/51.0'
>>> str(a.__add__(c))
'7.0/3.0'
>>> c.__add__(d)
NotImplemented
>>> d.__add__(a)
NotImplemented
>>> a + b
Ratio(26.0,51.0)
>>> b + c
Ratio(37.0,17.0)
>>> c + d
8.77
>>> d + a
7.103333333333333
>>>
'''

'''
>>> half = Ratio(1, 2)
>>> half
Ratio(1,2)
>>> print(half)
1/2
>>> half.__repr__()
'Ratio(1,2)'
>>> half.__str__()
'1/2'
>>>
'''

# special build-in method in python
# __init__
# __repr__
# __bool__
# __add__
# __float__
