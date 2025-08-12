scm> (define x (print 2))
2
x
scm> x
scm> (define (twice exp) (begin exp exp))
twice
scm> (twice (print 2))
2
scm> (define (twice exp) (list 'begin exp exp))
twice
scm> (twice (print 2))
2
(begin undefined undefined)
scm> (eval (print 2))
2
scm> (twice '(print 2))
(begin (print 2) (print 2))
scm> (eval (twice '(print 2)))
2
2
scm> (define-macro (twice expr) (list 'begin expr expr))
twice
scm> (twice (print 2))
2
2

(define-macro (check expr) 
    (list 
    'if expr ''passed
    (list 'quote (list 'failed: expr))
    )
)