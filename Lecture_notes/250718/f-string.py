# string concatenation
'''
>>> 'pi starts with ' + str(pi) + '...'
'pi starts with 3.141592653589793...'
'''
# string interpolation
'''
>>> f'pi starts with {pi} ...'
'pi starts with 3.141592653589793 ...'
'''

'''
>>> f'2 + 2 = {2 + 2}'
'2 + 2 = 4'
>>> f'2 + 2 = {abs(2 + 2)}'
'2 + 2 = 4'
>>> abs = float
>>> f'2 + 2 = {abs(2 + 2)}'
'2 + 2 = 4.0'
>>> f'2 + 2 = {(lambda x: x + x)(2)}'
'2 + 2 = 4'
'''
'''
>>> half
Fraction(1, 2)
>>> print(half)
1/2
>>> f'half of a half is {half * half}'
'half of a half is 1/4'
>>> f'half of a half is {str(half * half)}'
'half of a half is 1/4'
>>> f'half of a half is {repr(half * half)}'
'half of a half is Fraction(1, 4)'
'''