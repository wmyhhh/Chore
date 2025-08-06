def calc_eval(exp):
    if type(exp) in (int, float):
        return exp
    elif isinstance(exp, Pair):
        arguments = exp.second.map(calc_eval)
        return calc_apply(exp.first, arguments)
    else:
        raise TypeError

from operator import add, mul, truediv, sub

def reduce(f, s, initial):
    '''
    >>> reduce(mul, [2, 4, 8], 1)
    64
    >>> reduce(add, [1, 2, 3, 4], 0)
    10
    '''
    for i in s:
        initial = f(initial, i) # pay attention to the order!
    return initial

def calc_apply(operator, args):
    if not isinstance(operator, str):
        raise TypeError(str(operator) + 'is not a symbol')
    elif str(operator) == '+':
        return reduce(add, args, 0)

    elif str(operator) == '-':
        if len(args) == 0:
            raise TypeError(operator + 'take at least one argument')
        elif len(args) == 1:
            return -args.first
        else:
            return reduce(sub, args.second, args.first)
        
    elif str(operator) == '*':
        return reduce(mul, args, 1)
    elif str(operator) == '/':
        if len(args) == 0:
            raise TypeError(operator + 'require at least one argument')
        elif len(operator) == 1:
            return 1 / args.first
        else:
            return reduce(truediv, args.second, args.first)
    else:
        raise TypeError(str(operator) + 'is an unknown operator')